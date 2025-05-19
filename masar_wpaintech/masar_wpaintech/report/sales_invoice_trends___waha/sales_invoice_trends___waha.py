# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
	if not filters:
		filters = {}
	data = []
	conditions = get_columns(filters, "Sales Invoice")
	data = get_data(filters, conditions)

	return conditions["columns"], data


def get_columns(filters, trans):
	validate_filters(filters)

	based_on_details = based_wise_columns_query(filters.get("based_on"), trans)
	period_cols, period_select = period_wise_columns_query(filters, trans)
	group_by_cols = group_wise_column(filters.get("group_by"))

	columns = (
		based_on_details["based_on_cols"]
		+ period_cols
		+ [_("Total(Qty)") + ":Float:120", _("Total(Amt)") + ":Currency:120"]
	)
	if group_by_cols:
		columns = (
			based_on_details["based_on_cols"]
			+ group_by_cols
			+ period_cols
			+ [_("Total(Qty)") + ":Float:120", _("Total(Amt)") + ":Currency:120"]
		)

	conditions = {
		"based_on_select": based_on_details["based_on_select"],
		"period_wise_select": period_select,
		"columns": columns,
		"group_by": based_on_details["based_on_group_by"],
		"grbc": group_by_cols,
		"trans": trans,
		"addl_tables": based_on_details["addl_tables"],
		"addl_tables_relational_cond": based_on_details.get("addl_tables_relational_cond", ""),
	}

	return conditions

def validate_filters(filters):
	for f in ["From Date", "To Date", "Based On", "Company"]:
		if not filters.get(f.lower().replace(" ", "_")):
			frappe.throw(_("{0} is mandatory").format(f))

	if filters.get("based_on") == filters.get("group_by"):
		frappe.throw(_("'Based On' and 'Group By' can not be same"))

def get_data(filters, conditions):
	data = []
	inc, cond = "", ""
	query_details = conditions["based_on_select"] + conditions["period_wise_select"]

	posting_date = "t1.transaction_date"
	if conditions.get("trans") in [
		"Sales Invoice",
		"Purchase Invoice",
		"Purchase Receipt",
		"Delivery Note",
	]:
		posting_date = "t1.posting_date"
		if filters.period_based_on:
			posting_date = "t1." + filters.period_based_on

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if filters.get("group_by"):
		sel_col = ""
		ind = conditions["columns"].index(conditions["grbc"][0])

		if filters.get("group_by") == "Item":
			sel_col = "t2.item_code"
		elif filters.get("group_by") == "Customer":
			sel_col = "t1.customer"

		if filters.get("based_on") in ["Item", "Customer"]:
			inc = 2
		if filters.get("based_on") == "Customer" and filters.get("customer"):
			cond += f" and t1.customer = '{filters.get('customer')}'"

		
		data1 = frappe.db.sql(
			""" select {} from `tab{}` t1, `tab{} Item` t2 {}
					where t2.parent = t1.name and t1.company = {} and {} between {} and {} and
					t1.docstatus = 1 {} {}
					group by {}
				""".format(
				query_details,
				conditions["trans"],
				conditions["trans"],
				conditions["addl_tables"],
				"%s",
				posting_date,
				"%s",
				"%s",
				conditions.get("addl_tables_relational_cond"),
				cond,
				conditions["group_by"],
			),
			(filters.get("company"), from_date, to_date),
			as_list=1,
		)

		for d in range(len(data1)):
			# to add blanck column
			dt = data1[d]
			dt.insert(ind, "")
			dt.insert(ind, "")
			data.append(dt)

			# to get distinct value of col specified by group_by in filter
			row = frappe.db.sql(
				"""select DISTINCT({}) from `tab{}` t1, `tab{} Item` t2 {}
						where t2.parent = t1.name and t1.company = {} and {} between {} and {}
						and t1.docstatus = 1 and {} = {} {} {}
					""".format(
					sel_col,
					conditions["trans"],
					conditions["trans"],
					conditions["addl_tables"],
					"%s",
					posting_date,
					"%s",
					"%s",
					conditions["group_by"],
					"%s",
					conditions.get("addl_tables_relational_cond"),
					cond,
				),
				(filters.get("company"), from_date, to_date, data1[d][0]),
				as_list=1,
			)

			for i in range(len(row)):
				des = ["" for q in range(len(conditions["columns"]))]

				# get data for group_by filter
				row1 = frappe.db.sql(
					""" select t2.item_code, t2.description, {} from `tab{}` t1, `tab{} Item` t2 {}
							where t2.parent = t1.name and t1.company = {} and {} between {} and {}
							and t1.docstatus = 1 and {} = {} and {} = {} {} {}
						""".format(
						conditions["period_wise_select"],
						conditions["trans"],
						conditions["trans"],
						conditions["addl_tables"],
						"%s",
						posting_date,
						"%s",
						"%s",
						sel_col,
						"%s",
						conditions["group_by"],
						"%s",
						conditions.get("addl_tables_relational_cond"),
						cond,
					),
					(filters.get("company"), from_date, to_date, row[i][0], data1[d][0]),
					as_list=1,
				)

				des[ind] = row[i][0]  # item_code
				des[ind + 1] = row1[0][1]  # description

				for j in range(1, len(conditions["columns"]) - inc):
					des[j + inc] = row1[0][j]
				frappe.msgprint(str(des))
				data.append(des)
	else:
		data = frappe.db.sql(
			""" select {} from `tab{}` t1, `tab{} Item` t2 {}
					where t2.parent = t1.name and t1.company = {} and {} between {} and {} and
					t1.docstatus = 1 {} {}
					group by {}
				""".format(
				query_details,
				conditions["trans"],
				conditions["trans"],
				conditions["addl_tables"],
				"%s",
				posting_date,
				"%s",
				"%s",
				cond,
				conditions.get("addl_tables_relational_cond", ""),
				conditions["group_by"],
			),
			(filters.get("company"), from_date, to_date),
			as_list=1,
		)
	frappe.msgprint(str(data))
	return data

def period_wise_columns_query(filters, trans):
	query_details = ""
	pwc = []

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if trans in ["Purchase Receipt", "Delivery Note", "Purchase Invoice", "Sales Invoice"]:
		trans_date = filters.period_based_on or "posting_date"
	else:
		trans_date = "transaction_date"

	pwc = [
		"Qty:Float:120",
		"Amount:Currency:120",
	]

	query_details = f"""
		SUM(IF(t1.{trans_date} BETWEEN '{from_date}' AND '{to_date}', t2.stock_qty, 0)),
		SUM(IF(t1.{trans_date} BETWEEN '{from_date}' AND '{to_date}', t2.base_net_amount, 0)),
	"""

	query_details += "SUM(t2.stock_qty), SUM(t2.base_net_amount)"
	return pwc, query_details

def based_wise_columns_query(based_on, trans):
	based_on_details = {}

	if based_on == "Item":
		based_on_details["based_on_cols"] = ["Item:Link/Item:120", "Description:Data:300"]
		based_on_details["based_on_select"] = "t2.item_code, t2.description,"
		based_on_details["based_on_group_by"] = "t2.item_code"
		based_on_details["addl_tables"] = ""

	elif based_on == "Customer":
		based_on_details["based_on_cols"] = [
			"Customer:Link/Customer:120",
			"Territory:Link/Territory:120",
		]
		based_on_details["based_on_select"] = "t1.customer_name, t1.territory,"
		based_on_details["based_on_group_by"] = "t1.customer"
		based_on_details["addl_tables"] = ""

	return based_on_details

def group_wise_column(group_by):
	if group_by == "Item":
		return ["Item:Link/Item:120", "Description:Data:250"]
	elif group_by:
		return [group_by + ":Link/" + group_by + ":120"]
	else:
		return []