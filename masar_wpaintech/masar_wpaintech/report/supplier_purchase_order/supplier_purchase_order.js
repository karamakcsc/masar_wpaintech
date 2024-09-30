// Copyright (c) 2024, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Supplier Purchase Order"] = {
	"filters": [
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
