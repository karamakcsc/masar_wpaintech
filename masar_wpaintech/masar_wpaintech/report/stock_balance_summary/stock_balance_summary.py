# Copyright (c) 2026, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate
import erpnext


def execute(filters=None):
    return StockBalanceReport(filters).run()


class StockBalanceReport:
	def __init__(self, filters=None):
		self.filters = filters or {}
		self.from_date = getdate(self.filters.get("from_date"))
		self.to_date = getdate(self.filters.get("to_date"))
		self.data = []

		if self.filters.get("company"):
			self.company_currency = erpnext.get_company_currency(
				self.filters.get("company")
			)
		else:
			self.company_currency = frappe.db.get_single_value(
				"Global Defaults", "default_currency"
			)

	def run(self):
		self.prepare_data()
		return self.get_columns(), self.data

	def prepare_data(self):
		sle = frappe.qb.DocType("Stock Ledger Entry")
		item = frappe.qb.DocType("Item")

		query = (
			frappe.qb.from_(sle)
			.inner_join(item)
			.on(sle.item_code == item.name)
			.select(
				sle.item_code,
				item.item_name,
				item.item_group,
				item.brand,
				sle.warehouse,
				item.stock_uom,
				sle.actual_qty,
				sle.stock_value_difference,
				sle.valuation_rate,
			)
			.where(
				(sle.docstatus < 2)
				& (sle.is_cancelled == 0)
				& (sle.posting_date <= self.to_date)
			)
		)

		if self.filters.get("company"):
			query = query.where(sle.company == self.filters.get("company"))

		if self.filters.get("item_group"):
			query = query.where(item.item_group == self.filters.get("item_group"))

		if self.filters.get("item_code"):
			query = query.where(item.name.isin(self.filters.get("item_code")))

		if self.filters.get("brand"):
			query = query.where(item.brand == self.filters.get("brand"))

		if self.filters.get("warehouse"):
			query = query.where(sle.warehouse.isin(self.filters.get("warehouse")))

		entries = query.run(as_dict=True)

		item_map = {}

		for d in entries:
			key = (d.item_code, d.warehouse)

			if key not in item_map:
				item_map[key] = frappe._dict({
					"item_code": d.item_code,
					"item_name": d.item_name,
					"item_group": d.item_group,
					"brand": d.brand,
					"warehouse": d.warehouse,
					"stock_uom": d.stock_uom,
					"bal_qty": 0.0,
					"bal_val": 0.0,
					"val_rate": 0.0,
				})

			item_map[key].bal_qty += flt(d.actual_qty)
			item_map[key].bal_val = flt(item_map[key].bal_val + flt(d.stock_value_difference), 2)
			item_map[key].val_rate = flt(d.valuation_rate, 2)

		self.data = list(item_map.values())

	def get_columns(self):
		return [
			{
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 150,
			},
			{
				"label": _("Item Name"),
				"fieldname": "item_name",
				"width": 200,
			},
			{
				"label": _("Item Group"),
				"fieldname": "item_group",
				"fieldtype": "Link",
				"options": "Item Group",
				"width": 150,
			},
			{
				"label": _("Brand"),
				"fieldname": "brand",
				"fieldtype": "Link",
				"options": "Brand",
				"width": 120,
			},
			{
				"label": _("Warehouse"),
				"fieldname": "warehouse",
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 140,
			},
			{
				"label": _("Stock UOM"),
				"fieldname": "stock_uom",
				"fieldtype": "Link",
				"options": "UOM",
				"width": 90,
			},
			{
				"label": _("Balance Qty"),
				"fieldname": "bal_qty",
				"fieldtype": "Int",
				"width": 135,
				"precision": 0,
			},
			{
				"label": _("Valuation Rate"),
				"fieldname": "val_rate",
				"fieldtype": "Currency",
				"options": "Company:company:default_currency",
				"width": 150,
			},
			{
				"label": _("Balance Value"),
				"fieldname": "bal_val",
				"fieldtype": "Currency",
				"options": "Company:company:default_currency",
				"width": 150,
			},
		]
