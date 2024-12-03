// Copyright (c) 2024, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Waha Purchase Receipt"] = {
	"filters": [
		{
			"fieldname": "name",
			"label": __("Purchase Receipt"),
			"fieldtype": "Link",
			"options": "Purchase Receipt",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "ref_no",
			"label": __("Reference Number"),
			"fieldtype": "Data",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "from",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "to",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 100,
			"reqd": 0,
		},
	]
};
