# Copyright (c) 2024, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(), data(filters), None

def data(filters):
    conditions = ""
    
    if filters.get("item_code"):
        conditions += f"AND tpoi.item_code = '{filters.get('item_code')}'"
	
    if filters.get("supplier"):
        conditions += f"AND tpo.supplier = '{filters.get('supplier')}'"
    
    data = frappe.db.sql(f"""
                         SELECT 
							tpoi.idx, tpoi.item_code, tpo.supplier, tpoi.description, tpoi.uom, 
							tpoi.qty, tpoi.price_list_rate, tpoi.rate, tpo.total, tpoi.custom_no_cartron, tpo.total_net_weight 
						FROM `tabPurchase Order` tpo
						INNER JOIN `tabPurchase Order Item` tpoi ON tpoi.parent = tpo.name
						WHERE 1=1 {conditions}
                         """)
    
    return data

def columns():
    return [
		"Serial No.: Int:100",
		"Item Code: Link/Item Code:200",
		"Supplier Code: Link/Supplier:100",
		"Description: Data:300",
		"UOM: Link/UOM:100",
		"Qty: Float:100",
		"Price List Price: Currency:125",
		"Rate: Currency:100",
		"Total: Currency:100",
		"Cartons No.: Float:100",
		"Gross Weight: Float:100",
	]