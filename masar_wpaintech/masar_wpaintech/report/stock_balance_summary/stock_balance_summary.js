// Copyright (c) 2026, KCSC and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance Summary"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_default("company"),
			reqd: 1,
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
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			options: "Brand",
		},
		{
			fieldname: "item_code",
			label: __("Items"),
			fieldtype: "MultiSelectList",
			options: "Item",
			get_data: async function (txt) {
				let item_group = frappe.query_report.get_filter_value("item_group");

				let filters = {
					is_stock_item: 1,
					...(item_group && { item_group }),
				};

				let { message } = await frappe.call({
					method: "erpnext.controllers.queries.item_query",
					args: {
						doctype: "Item",
						txt: txt,
						searchfield: "name",
						start: 0,
						page_len: 20,
						filters: filters,
					},
				});

				return message || [];
			},
		},
		{
			fieldname: "warehouse",
			label: __("Warehouses"),
			fieldtype: "MultiSelectList",
			options: "Warehouse",
			get_data: function (txt) {
				let company = frappe.query_report.get_filter_value("company");
				return frappe.db.get_link_options("Warehouse", txt, {
					...(company && { company }),
				});
			},
		},
	],

	onload: function (report) {
		report.page.add_inner_button(__("View Stock Ledger"), function () {
			let filters = report.get_values();
			frappe.set_route("query-report", "Stock Ledger", filters);
		});
	},
};
