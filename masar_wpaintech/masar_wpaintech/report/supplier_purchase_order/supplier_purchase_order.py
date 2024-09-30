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
							tpoi.qty, tpoi.custom_carton_capacity, tpoi.custom_no_cartron, tpoi.weight_per_unit, tpoi.total_weight, tpo.total_net_weight
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
		"Qty Per Caton: float:125",
		"Cartons No.: Float:100",
		"Weight Per Unit: Float:100",
		"Total Weight: Float:100",
		"Gross Weight: Float:100",
	]