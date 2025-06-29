# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	return columns(filters), data(filters)

def data(filters):
    conditions=' 1=1 '
    if filters.get('customer'):
        conditions += f' AND tsi.customer ="{filters.get("customer")}"'
    if filters.get('name'):
         conditions += f' AND tsi.name ="{filters.get("name")}"'    
    if filters.get('status'):
        conditions += f' AND tsi.status = "{filters.get("status")}"'
    _from, to = filters.get("from_date"), filters.get("to_date")
    if _from and to:
        conditions += f" AND tsi.posting_date BETWEEN '{_from}' AND '{to}'"
          
    sql = frappe.db.sql(f"""SELECT 
								tsi.name AS `Sales Invoice`,
								tsi.customer AS Customer,
								tsi.customer_name AS `Customer Name`,
								tsi.posting_date AS `Invoice Date`,
								tsi.total AS `Net Total`,
								tsi.total_taxes_and_charges AS `Total Taxes and Charges`,
								tsi.grand_total AS `Grand Total`,
								tsi.status AS Status
							FROM `tabSales Invoice` tsi
							WHERE {conditions} AND tsi.docstatus > 0
                                
        """)
    return sql


def columns(filters=None):
    columns = [
         "Sales Invoice:Link/Sales Invoice:200",
         "Customer:Link/Customer:200",
         "Customer Name: Data:200",
         "Invoice Date:Date:200",
         "Net Total:Currency:200",
         "Total Taxes and Charges:Currency:200",
         "Grand Total:Currency:200",
         "Status:Data:200",
	]
    
    return columns