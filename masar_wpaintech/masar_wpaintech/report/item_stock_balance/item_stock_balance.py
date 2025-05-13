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
        
    if filters.get("group_by"):
        group_by_fiter = filters.get("group_by")
        if group_by_fiter == "Warehouse":
            select = "tb.warehouse,"
            group_by = "tb.item_code, tb.warehouse"
        elif group_by_fiter == "Item":
            select = "All Warehouses,"
            group_by = "tb.item_code"
            
    sql = frappe.db.sql(f"""
		WITH po AS(
			SELECT 
				tpo.name AS name,
				tpoi.item_code,
				tpoi.qty AS pending_order
			FROM `tabPurchase Order` tpo 
			INNER JOIN `tabPurchase Order Item` tpoi ON tpo.name = tpoi.parent
			WHERE tpo.docstatus = 0
		)
		SELECT DISTINCT
			tb.item_code AS `Item Code`,
			ti.item_name AS `Item Name`,
			ti.custom_manufacturing_code AS `Manufacturing Code`,
			ti.brand AS `Brand`,
			tb.stock_uom AS `Stock UOM`,
			{select}
			SUM(tb.actual_qty) AS `Stock Balance`,
			AVG(tb.valuation_rate) AS `Valuation Rate`,
			SUM(IFNULL(po.pending_order, 0)) AS `Pending Qty`
		FROM `tabBin` tb 
		INNER JOIN `tabItem` ti ON tb.item_code = ti.name
		LEFT JOIN po ON tb.item_code = po.item_code
		WHERE {conditions} AND tb.warehouse NOT IN ('Stores - WP')
		GROUP BY {group_by}
	""")
    
    return sql


def columns(filters=None):
	columns = [
		"Item Code:Data:150",
		"Item Name:Data:150",
		"Manufacturing Code:150",
		"Brand:Link/Brand:100",
		"Stock UOM:Data:100",
		"Qty Per Carton:Float:125",
		"Warehouse:Link/Warehouse:150",
		"Stock Balance:Float:150",
		"Valuation Rate:Currency:150",
		"Pending Qty:Float:150",
	]
	return columns