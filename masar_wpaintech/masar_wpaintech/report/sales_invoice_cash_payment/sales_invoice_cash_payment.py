# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	return columns(), data(filters)

def data(filters):
    conditions=' 1=1 '
    if filters.get('customer'):
        conditions += f' AND tsi.customer ="{filters.get("customer")}"'
    if filters.get('payment_type'):
        conditions += f' AND tsi.custom_payment_type ="{filters.get("payment_type")}"'
    if filters.get('name'):
         conditions += f' AND tsi.name ="{filters.get("name")}"'    
    if filters.get('status'):
        conditions += f' AND tsi.status = "{filters.get("status")}"'
    _from, to = filters.get("from_date"), filters.get("to_date")
    if _from and to:
        conditions += f""" 
            AND (
                (tpe.posting_date IS NOT NULL AND tpe.posting_date BETWEEN "{_from}" AND "{to}")
                OR 
                (tpe.posting_date IS NULL AND tsi.posting_date BETWEEN "{_from}" AND "{to}")
            )
        """
         
    sql = frappe.db.sql(f"""SELECT 
                                tsi.name,
                                tsi.customer,
                                COALESCE(NULLIF(tsi.custom_customer_name_en, ''), tsi.customer_name) AS `Customer Name`,
                                tsi.posting_date,
                                tsi.grand_total,
                                tsi.custom_payment_type,
                                tsi.status,
                                tpe.posting_date,
                                tpe.mode_of_payment
                            FROM `tabSales Invoice` tsi
                            LEFT JOIN `tabPayment Entry Reference` tper ON tper.reference_name = tsi.name AND tper.docstatus = 1
                            LEFT JOIN `tabPayment Entry` tpe ON tpe.name = tper.parent AND tpe.docstatus = 1
                            WHERE {conditions}  AND tsi.docstatus = 1;
""")
    return sql


def columns():
    return[
         "Sales Invoice:Link/Sales Invoice:200",
         "Customer:Link/Customer:200",
         "Customer Name: Data:200",
         "Posting Date:Date:200",
         "Grand Total:Currency:200",
         "Payment Type:Data:200",
         "Status:Data:200",
         "Payment Date: Date:200",
         "Mode of Payment: Data:200",
	]