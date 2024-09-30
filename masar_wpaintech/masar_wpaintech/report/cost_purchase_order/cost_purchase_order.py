# Copyright (c) 2024, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(), data(filters), None

def data(filters):
    conditions = ""
    
    _from, to = filters.get('from'), filters.get('to')
    
    if filters.get("name"):
        conditions += f"AND tpo.name = '{filters.get('name')}'"
    
    if filters.get("item_code"):
        conditions += f"AND tpoi.item_code = '{filters.get('item_code')}'"
	
    if filters.get("supplier"):
        conditions += f"AND tpo.supplier = '{filters.get('supplier')}'"
        
    if _from and to:
        conditions += f"AND tpo.transaction_date BETWEEN '{_from}' AND '{to}'"
    
    data = frappe.db.sql(f"""
                         SELECT 
							tpo.name, tpo.transaction_date, tpoi.item_code, tpo.supplier, tpo.supplier_name, tpoi.description, tpoi.uom,
							tpoi.qty, tpoi.custom_carton_capacity, tpoi.custom_no_cartron, tpoi.weight_per_unit, 
       						tpoi.total_weight, tpo.total_net_weight
						FROM `tabPurchase Order` tpo
						INNER JOIN `tabPurchase Order Item` tpoi ON tpoi.parent = tpo.name
						WHERE 1=1 {conditions}
                         """)
    
    return data

def columns():
    return [
		"Purchase Order: Link/Purchase Order:150",
		"Posting Date: Date:150",
		"Item Code: Link/Item Code:150",
		"Supplier Code: Link/Supplier:125",
		"Supplier Name: Data:125",
		"Description: Data:300",
		"UOM: Link/UOM:100",
		"Qty: Float:100",
		"Price List Price: Currency:125",
		"Rate: Currency:100",
		"Total: Currency:100",
		"Cartons No.: Float:150",
		"Gross Weight: Float:150",
	]