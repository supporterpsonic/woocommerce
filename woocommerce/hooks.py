# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "woocommerce"
app_title = "WooCommerce"
app_publisher = "WooCommerce"
app_description = "WooCommerce"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "technical@erpsonic.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/woocommerce/css/woocommerce.css"
# app_include_js = "/assets/woocommerce/js/woocommerce.js"

# include js, css files in header of web template
# web_include_css = "/assets/woocommerce/css/woocommerce.css"
# web_include_js = "/assets/woocommerce/js/woocommerce.js"

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

# Website user home page (by function)
# get_website_user_home_page = "woocommerce.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "woocommerce.install.before_install"
# after_install = "woocommerce.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "woocommerce.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }


doc_events = {
	"Item": {
		"validate": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.membuat_atau_update_item_baru",
		"on_trash": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.hapus_item_woocommerce",
		
	},
	"Stock Entry": {
		"on_submit": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.submit_cancel_document_stock_entry",
		"on_cancel": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.submit_cancel_document_stock_entry",
		
	},
	"Purchase Receipt": {
		"on_submit": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.submit_cancel_document_purchase_receipt",
		"on_cancel": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.submit_cancel_document_purchase_receipt",
		
	},
	"Stock Reconciliation": {
		"on_submit": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.submit_cancel_document_stock_reconcilliation",
		"on_cancel": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.submit_cancel_document_stock_reconcilliation",
		
	},
	"Item Price": {
		"validate": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.add_edit_item_price",
		"on_trash": "woocommerce.woocommerce.doctype.woo_setting.woo_setting.delete_item_price",
		
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"woocommerce.tasks.all"
# 	],
# 	"daily": [
# 		"woocommerce.tasks.daily"
# 	],
# 	"hourly": [
# 		"woocommerce.tasks.hourly"
# 	],
# 	"weekly": [
# 		"woocommerce.tasks.weekly"
# 	]
# 	"monthly": [
# 		"woocommerce.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "woocommerce.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "woocommerce.event.get_events"
# }

