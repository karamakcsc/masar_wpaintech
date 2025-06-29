// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Invoice Summary"] = {
	"filters": [
		{
			"fieldname":"name",
			"label":"Sales Invoice",
			"fieldtype":"Link",
			"options": "Sales Invoice"
		},
		{
			"fieldname":"customer",
			"label":"Customer",
			"fieldtype": "Link",
			"options": "Customer"
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
		{
			"fieldname":"status",
			"label":"Status",
			"fieldtype":"Select",
			"options": "\nPaid\nUnpaid\nPartialy Paid\nOverdue\nReturn"
		},
	]
};
