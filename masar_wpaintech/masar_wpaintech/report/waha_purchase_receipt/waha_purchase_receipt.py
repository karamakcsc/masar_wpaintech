# Copyright (c) 2024, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
    conditions = " 1=1 "
    if filters.get('name'):
        conditions += f" AND tpr.name = '{filters.get('name')}'"
    if filters.get('ref_no'):
        conditions += f" AND tpr.custom_ref_number LIKE '%{filters.get('ref_no')}%'"
    if filters.get('item_code'):
        conditions += f" AND tpri.item_code = '{filters.get('item_code')}'"
    _from, to = filters.get('from'), filters.get('to')
    if _from and to:
        conditions += f" AND tpr.posting_Date BETWEEN '{_from}' AND '{to}'"
    
    sql = frappe.db.sql(f"""
                        SELECT 
							tpr.name AS `ID`, 
							tpr.custom_ref_number AS `Reference Number`, 
							tpr.posting_date AS `Date`, 
							tpr.currency AS `Currency`, 
							tpr.supplier_name AS `Supplier Name`, 
							tpri.item_code AS `Item Code`,
							tpri.item_name AS `Item Name`,
							tpri.uom AS `UOM`,
							tpri.qty AS `Qty`,
							tpri.rate AS `Rate`,
							tpri.net_amount AS `Net Amount`,
							tpri.landed_cost_voucher_amount AS `Landed Cost Amount`
						FROM 
      						`tabPurchase Receipt` tpr 
						INNER JOIN 
      						`tabPurchase Receipt Item` tpri ON tpri.parent = tpr.name 
						WHERE 
      						{conditions} AND tpr.docstatus = 1
                        """)
    
    return sql

def get_columns():
    return [
        "ID: Link/Purchase Receipt:200",
		"Reference Number: Data:200",
		"Posting Date: Date:200",
		"Currency: Link/Currency:200",
		"Supplier Name: Data:200",
		"Item Code: Link/Item:200",
		"Item Name: Data:200",
		"UOM: Link/UOM:200",
		"Qty: Float:200",
		"Rate: Currency:200",
		"Net Amount: Currency:200",
		"Landed Cost Amount: Currency:250"
	]
