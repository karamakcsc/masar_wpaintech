// Copyright (c) 2025, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Invoice Trends - Waha"] = {
	"filters": [
		// {
		// 	fieldname: "period",
		// 	label: __("Period"),
		// 	fieldtype: "Select",
		// 	options: [
		// 		{ value: "Monthly", label: __("Monthly") },
		// 		{ value: "Quarterly", label: __("Quarterly") },
		// 		{ value: "Half-Yearly", label: __("Half-Yearly") },
		// 		{ value: "Yearly", label: __("Yearly") },
		// 	],
		// 	default: "Monthly",
		// },
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: [
				{ value: "Item", label: __("Item") },
				{ value: "Customer", label: __("Customer") },
				{ value: "Brand", label: __("Brand") },
			],
			default: "Customer",
			dashboard_config: {
				read_only: 1,
			},
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: ["", { value: "Item", label: __("Item") }, { value: "Customer", label: __("Customer") }, { value: "Brand", label: __("Brand") },],
			default: "Item",
		},
		// {
		// 	fieldname: "fiscal_year",
		// 	label: __("Fiscal Year"),
		// 	fieldtype: "Link",
		// 	options: "Fiscal Year",
		// 	default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today()),
		// },
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
	]
};
