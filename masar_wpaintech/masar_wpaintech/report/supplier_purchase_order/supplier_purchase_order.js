// Copyright (c) 2024, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Supplier Purchase Order"] = {
	"filters": [
		{
			fieldname: "name",
			label: __("Purchase Order"),
			fieldtype: "Link",
			options: "Purchase Order"
		},
		{
			fieldname: "from",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to",
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options: "Item"
		},
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier"
		}
	]
};
