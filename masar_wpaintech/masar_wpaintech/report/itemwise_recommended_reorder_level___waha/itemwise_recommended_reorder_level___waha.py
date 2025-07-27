# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Abs, Sum
from frappe.utils import flt, getdate


def execute(filters=None):
	if not filters:
		filters = {}
	float_precision = frappe.db.get_default("float_precision")

	avg_daily_outgoing = 0
	diff = ((getdate(filters.get("to_date")) - getdate(filters.get("from_date"))).days) + 1
	if diff <= 0:
		frappe.throw(_("'From Date' must be after 'To Date'"))

	columns = get_columns()
	items = get_item_info(filters)
	consumed_item_map = get_consumed_items(filters)
	delivered_item_map = get_delivered_items(filters)
	bin_item_map = get_stock_balance(filters)
	po_pending_map = get_po_pending_qty(filters)

	data = []
	for item in items:
		stock_qty = flt(bin_item_map.get(item.name, 0))
		if filters.get("has_stock") and stock_qty <= 0:
			continue
		total_outgoing = flt(consumed_item_map.get(item.name, 0)) + flt(delivered_item_map.get(item.name, 0))
		avg_daily_outgoing = flt(total_outgoing / diff, float_precision)
		avg_monthly_outgoing = flt(avg_daily_outgoing * 30, float_precision)
		reorder_level = (avg_daily_outgoing * flt(item.lead_time_days)) + flt(item.safety_stock)
		po_pending_qty = flt(po_pending_map.get(item.name, 0))

		data.append(
			[
				item.name,
				item.custom_manufacturing_code,
				item.brand,
				item.description,
				item.stock_uom,
				item.safety_stock,
				item.lead_time_days,
				stock_qty,
				po_pending_qty,
				consumed_item_map.get(item.name, 0),
				delivered_item_map.get(item.name, 0),
				total_outgoing,
				avg_daily_outgoing,
				avg_monthly_outgoing,
				reorder_level,
			]
		)

	if filters.get("brand"):
		columns = [col for col in columns if not col.startswith(_("Brand"))]
		for row in data:
			del row[2]

	return columns, data


def get_columns():
	return [
		_("Item") + ":Link/Item:120",
		_("Manufacturing Code") + ":Data:120",
		_("Brand") + ":Link/Brand:100",
		_("Description") + "::250",
		_("Stock UOM") + ":Link/UOM:100",
		_("Safety Stock") + ":Float:160",
		_("Lead Time Days") + ":Float:120",
		_("Stock Balance") + ":Float:120",
		_("Pending Qty") + ":Float:120",
		_("Consumed") + ":Float:120",
		_("Delivered") + ":Float:120",
		_("Total Outgoing") + ":Float:120",
		_("Avg Daily Outgoing") + ":Float:160",
		_("Avg Monthly Outgoing") + ":Float:160",
		_("Reorder Level") + ":Float:120",
	]


def get_item_info(filters):
	item = frappe.qb.DocType("Item")
	query = (
		frappe.qb.from_(item)
		.select(
			item.name,
			item.custom_manufacturing_code,
			item.description,
			item.stock_uom,
			item.brand,
			item.safety_stock,
			item.lead_time_days,
		)
		.where((item.is_stock_item == 1) & (item.disabled == 0))
	)

	if brand := filters.get("brand"):
		query = query.where(item.brand == brand)

	return query.run(as_dict=True)


def get_consumed_items(filters):
	purpose_to_exclude = [
		"Material Transfer for Manufacture",
		"Material Transfer",
		"Send to Subcontractor",
	]

	se = frappe.qb.DocType("Stock Entry")
	sle = frappe.qb.DocType("Stock Ledger Entry")
	query = (
		frappe.qb.from_(sle)
		.left_join(se)
		.on(sle.voucher_no == se.name)
		.select(sle.item_code, Abs(Sum(sle.actual_qty)).as_("consumed_qty"))
		.where(
			(sle.actual_qty < 0)
			& (sle.is_cancelled == 0)
			& (sle.voucher_type.notin(["Delivery Note", "Sales Invoice"]))
			& ((se.purpose.isnull()) | (se.purpose.notin(purpose_to_exclude)))
		)
		.groupby(sle.item_code)
	)
	query = get_filtered_query(filters, sle, query)

	consumed_items = query.run(as_dict=True)

	return {item.item_code: item.consumed_qty for item in consumed_items}


def get_delivered_items(filters):
	parent = frappe.qb.DocType("Delivery Note")
	child = frappe.qb.DocType("Delivery Note Item")
	query = (
		frappe.qb.from_(parent)
		.from_(child)
		.select(child.item_code, Sum(child.stock_qty).as_("dn_qty"))
		.where((parent.name == child.parent) & (parent.docstatus == 1))
		.groupby(child.item_code)
	)
	query = get_filtered_query(filters, parent, query)

	dn_items = query.run(as_dict=True)

	parent = frappe.qb.DocType("Sales Invoice")
	child = frappe.qb.DocType("Sales Invoice Item")
	query = (
		frappe.qb.from_(parent)
		.from_(child)
		.select(child.item_code, Sum(child.stock_qty).as_("si_qty"))
		.where((parent.name == child.parent) & (parent.docstatus == 1) & (parent.update_stock == 1))
		.groupby(child.item_code)
	)
	query = get_filtered_query(filters, parent, query)

	si_items = query.run(as_dict=True)

	dn_item_map = {}
	for item in dn_items:
		dn_item_map[item.item_code] = item.dn_qty

	for item in si_items:
		if item.item_code in dn_item_map:
			dn_item_map[item.item_code] += item.si_qty
		else:
			dn_item_map[item.item_code] = item.si_qty

	return dn_item_map


def get_stock_balance(filters):
	bin = frappe.qb.DocType("Bin")
	query = (
		frappe.qb.from_(bin)
		.select(bin.item_code, Sum(bin.actual_qty).as_("stock_qty"))
		.groupby(bin.item_code)
	)

	if filters.get("has_stock"):
		query = query.where(bin.actual_qty > 0)

	bin_items = query.run(as_dict=True)

	return {item.item_code: item.stock_qty for item in bin_items}


def get_po_pending_qty(filters):
	po = frappe.qb.DocType("Purchase Order")
	poi = frappe.qb.DocType("Purchase Order Item")

	query = (
		frappe.qb.from_(po)
		.from_(poi)
		.select(
			poi.item_code,
			Sum(poi.qty - poi.received_qty).as_("pending_qty")
		)
		.where(
			(po.name == poi.parent) &
			(po.docstatus < 2) &
			(po.status.notin(["Closed", "Completed", "Cancelled"])) &
			(poi.received_qty < poi.qty)
		)
		.groupby(poi.item_code)
	)

	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(po.transaction_date.between(filters["from_date"], filters["to_date"]))

	po_items = query.run(as_dict=True)

	return {item.item_code: item.pending_qty for item in po_items}


def get_filtered_query(filters, table, query):
	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(table.posting_date.between(filters["from_date"], filters["to_date"]))
	else:
		frappe.throw(_("From and To dates are required"))

	return query