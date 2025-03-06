// Copyright (c) 2025, KCSC and contributors
// For licenscustomere information, please see license.txt

frappe.query_reports["Sales Invoice Cash Payment"] = {
	"filters": [
		{
			"fieldname":"name",
			"label":"Sales Invoice",
			"fieldtype":"Data"
		},
		{
			"fieldname":"customer",
			"label":"Customer",
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"payment_type",
			"label":"Payment Type",
			"fieldtype":"Select",
			"options": "\nCash\nOn Account",		
		},
		{
			"fieldname":"from_date",
			"label":"From Date",
			"fieldtype":"Date"
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype":"Date"
		},
	]
};
