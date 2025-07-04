// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Itemwise Recommended Reorder Level - Waha"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			options: "Brand",
		},
		{
			fieldname: "has_stock",
			label: __("Has Stock"),
			fieldtype: "Check",
			default: 1,
		}
	]
};
