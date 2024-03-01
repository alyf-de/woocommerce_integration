app_name = "woocommerce_integration"
app_title = "Woocommerce-ERPNext Integration"
app_publisher = "ALYF GmbH"
app_description = "A WooCommerce Integration for ERPNext"
app_email = "hallo@alyf.de"
app_license = "MIT"

after_install = "woocommerce_integration.install.after_install"
after_uninstall = "woocommerce_integration.install.after_uninstall"

woocomm_custom_fields = {
    "Customer": [
        {
            "fieldname": "woocomm_customer_id",
            "label": "WooCommerce Customer ID",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "read_only": 1,
        }
    ],
    "Address": [
        {
            "fieldname": "woocomm_customer_id",
            "label": "WooCommerce Customer ID",
            "fieldtype": "Data",
            "insert_after": "disabled",
            "read_only": 1,
        }
    ],
    "Contact": [
        {
            "fieldname": "woocomm_customer_id",
            "label": "WooCommerce Customer ID",
            "fieldtype": "Data",
            "insert_after": "company_name",
            "read_only": 1,
        }
    ],
    "Sales Order": [
        {
            "fieldname": "woocomm_order_id",
            "label": "WooCommerce Order ID",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "read_only": 1,
        }
    ],
    "Item": [
        {
            "fieldname": "woocomm_product_id",
            "label": "WooCommerce Product ID",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "read_only": 1,
        }
    ],
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/woocommerce_integration/css/woocommerce_integration.css"
# app_include_js = "/assets/woocommerce_integration/js/woocommerce_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/woocommerce_integration/css/woocommerce_integration.css"
# web_include_js = "/assets/woocommerce_integration/js/woocommerce_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "woocommerce_integration/public/scss/website"

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

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "woocommerce_integration.utils.jinja_methods",
# 	"filters": "woocommerce_integration.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "woocommerce_integration.install.before_install"

# Uninstallation
# ------------

# before_uninstall = "woocommerce_integration.uninstall.before_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "woocommerce_integration.utils.before_app_install"
# after_app_install = "woocommerce_integration.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "woocommerce_integration.utils.before_app_uninstall"
# after_app_uninstall = "woocommerce_integration.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "woocommerce_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"woocommerce_integration.tasks.all"
# 	],
# 	"daily": [
# 		"woocommerce_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"woocommerce_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"woocommerce_integration.tasks.weekly"
# 	],
# 	"monthly": [
# 		"woocommerce_integration.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "woocommerce_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "woocommerce_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "woocommerce_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["woocommerce_integration.utils.before_request"]
# after_request = ["woocommerce_integration.utils.after_request"]

# Job Events
# ----------
# before_job = ["woocommerce_integration.utils.before_job"]
# after_job = ["woocommerce_integration.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"woocommerce_integration.auth.validate"
# ]

woocomm_custom_fields = {
    "Customer": [
        {
            "fieldname": "woocomm_customer_id",
            "label": "WooCommerce Customer ID",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "read_only": 1,
        }
    ],
    "Address": [
        {
            "fieldname": "woocomm_customer_id",
            "label": "WooCommerce Customer ID",
            "fieldtype": "Data",
            "insert_after": "disabled",
            "read_only": 1,
        }
    ],
    "Contact": [
        {
            "fieldname": "woocomm_customer_id",
            "label": "WooCommerce Customer ID",
            "fieldtype": "Data",
            "insert_after": "company_name",
            "read_only": 1,
        }
    ],
    "Sales Order": [
        {
            "fieldname": "woocomm_order_id",
            "label": "WooCommerce Order ID",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "read_only": 1,
        }
    ],
    "Item": [
        {
            "fieldname": "woocomm_product_id",
            "label": "WooCommerce Product ID",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "read_only": 1,
        }
    ],
}