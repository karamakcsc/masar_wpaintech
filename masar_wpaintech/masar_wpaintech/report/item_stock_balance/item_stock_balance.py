# Copyright (c) 2025, KCSC and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	return columns(filters), data(filters)

def data(filters):
    conditions = " 1=1 "
    if filters.get("item_code"):
        conditions += f" AND tb.item_code = '{filters.get('item_code')}'"
    if filters.get("warehouse"):
        conditions += f" AND tb.warehouse = '{filters.get('warehouse')}'"
    if filters.get("brand"):
        conditions += f" AND ti.brand = '{filters.get('brand')}'"
    if filters.get("item_group"):
        conditions += f" AND ti.item_group = '{filters.get('item_group')}'"
    
    
    sql = frappe.db.sql(f"""
        SELECT
			tb.item_code AS `Item Code`,
			ti.item_name AS `Item Name`,
			ti.item_group AS `Item Group`,
			ti.brand AS `Brand`,
			tb.stock_uom AS `UOM`,
			tb.warehouse AS `Warehouse`,
			tb.actual_qty AS `Stock Balance`,
			tb.valuation_rate AS `Valuation Rate`
		FROM `tabBin` tb
		INNER JOIN `tabItem` ti ON ti.item_code = tb.item_code
		WHERE {conditions}
	""")
    
    return sql


def columns(filters=None):
	columns = [
		"Item Code:Link/Item:200",
		"Item Name::200",
		"Item Group:Link/Item Group:200",
		"Brand:Link/Brand:200",
		"Stock UOM::100",
		"Warehouse:Link/Warehouse:200",
		"Stock Balance:Float:150",
		"Valuation Rate:Currency:150",
	]
	return columns