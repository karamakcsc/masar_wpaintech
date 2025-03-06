# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	return columns(), data(filters)

def data(filters):
    conditions=' 1=1 '
    if filters.get('customer'):
        conditions += f' AND customer ="{filters.get("customer")}"'
    if filters.get('payment_type'):
        conditions += f' AND payment_type ="{filters.get("payment_type")}"'
    if filters.get('name'):
         conditions += f' AND name ="{filters.get("name")}"'    
    _from, to = filters.get("from_date"), filters.get("to_date")
    if _from and to:
         conditions += f' AND posting_date BETWEEN "{_from}" AND "{to}"'
    sql = frappe.db.sql(f"""SELECT 
                                name, customer, posting_date, grand_total, custom_payment_type, status
                                FROM `tabSales Invoice` 
                                WHERE {conditions}  AND docstatus = 1;
""")
    return sql


def columns():
    return[
         "Sales Invoice:Data:200",
         "Customer:Link/Customer:200",
         "Posting Date:Date:200",
         "Grand Total:Currency:200",
         "Payment Type:Data:200",
         "Status:Data:200",
	]