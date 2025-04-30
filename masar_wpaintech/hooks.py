from . import __version__ as app_version

app_name = "masar_wpaintech"
app_title = "Masar Wpaintech"
app_publisher = "KCSC"
app_description = "Masar Wpaintech"
app_email = "info@kcsc.com.jo"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/masar_wpaintech/css/masar_wpaintech.css"
# app_include_js = "/assets/masar_wpaintech/js/masar_wpaintech.js"

# include js, css files in header of web template
# web_include_css = "/assets/masar_wpaintech/css/masar_wpaintech.css"
# web_include_js = "/assets/masar_wpaintech/js/masar_wpaintech.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "masar_wpaintech/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "masar_wpaintech.utils.jinja_methods",
#	"filters": "masar_wpaintech.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "masar_wpaintech.install.before_install"
# after_install = "masar_wpaintech.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "masar_wpaintech.uninstall.before_uninstall"
# after_uninstall = "masar_wpaintech.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "masar_wpaintech.utils.before_app_install"
# after_app_install = "masar_wpaintech.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "masar_wpaintech.utils.before_app_uninstall"
# after_app_uninstall = "masar_wpaintech.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "masar_wpaintech.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Landed Cost Voucher": {
# 		"validate": "masar_wpaintech.custom.landed_cost_voucher.landed_cost_voucher.validate"
# 	}
# }
doctype_js = {
    "Purchase Order" : "custom/purchase_order/purchase_order.js",
    "Purchase Receipt" : "custom/purchase_receipt/purchase_receipt.js",
    "Sales Invoice" : "custom/sales_invoice/sales_invoice.js",
    "Quotation": "custom/quotation/quotation.js"
    # "Landed Cost Voucher" : "custom/landed_cost_voucher/landed_cost_voucher.js"
    # "Item" : "custom/item/item.js"
}
# Scheduled Tasks
# ----------------

# scheduler_events = {
#	"all": [
#		"masar_wpaintech.tasks.all"
#	],
#	"daily": [
#		"masar_wpaintech.tasks.daily"
#	],
#	"hourly": [
#		"masar_wpaintech.tasks.hourly"
#	],
#	"weekly": [
#		"masar_wpaintech.tasks.weekly"
#	],
#	"monthly": [
#		"masar_wpaintech.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "masar_wpaintech.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "masar_wpaintech.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "masar_wpaintech.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["masar_wpaintech.utils.before_request"]
# after_request = ["masar_wpaintech.utils.after_request"]

# Job Events
# ----------
# before_job = ["masar_wpaintech.utils.before_job"]
# after_job = ["masar_wpaintech.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"masar_wpaintech.auth.validate"
# ]
fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
                "Customer-custom_ref_no",
                "Supplier-custom_ref_no",
                "Purchase Order Item-custom_rate_per_unit",
                "Item-custom_carton_capacity",
                "Purchase Order Item-custom_no_cartron",
                "Purchase Order Item-custom_carton_capacity",
                "Item Group-custom_group_code",
                "Item-custom_group_code",
                "Item-custom_manufacturing_code",
                "Item-custom_description_ar",
                "Item-custom_column_break_lb7yg",
                "Purchase Order-custom_shipping_terms",
                "Purchase Order-custom_freight_type",
                "Purchase Order-custom_ref_number",
                "Purchase Order Item-custom_manufacturing_code",
                "Purchase Receipt-custom_ref_number",
                "Purchase Receipt Item-custom_manufacturing_code",
                "Purchase Receipt Item-custom_rate_per_unit",
                "Purchase Receipt Item-custom_carton_capacity",
                "Purchase Receipt Item-custom_no_carton",
                "Purchase Receipt-custom_total_landed_cost_amount",
                "Landed Cost Item-custom_percentage",
                "Purchase Receipt-custom_shipping_terms",
                "Landed Cost Item-custom_cnf",
                "Landed Cost Item-custom_total_cost",
                "Landed Cost Item-custom_total_amount",
                "Landed Cost Purchase Receipt-custom_reference_number",
                "Sales Invoice-custom_payment_type",
                "Sales Invoice-custom_customer_name_en",
                "Journal Entry Account-custom_masar_ref_no",
                "Purchase Invoice-custom_ref_number",
                "Purchase Receipt-custom_bill_date",
                "Purchase Receipt-custom_bill_no"
            ]
        ]
    ]},
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                [
                    "Sales Invoice-update_stock-default"
                ]
            ]
        ]
    }
]