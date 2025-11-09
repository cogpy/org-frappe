# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "odoo_to_erpnext"
app_title = "Odoo to ERPNext"
app_publisher = "Frappe + Anybox"
app_description = "Migrate your Odoo database to erpnext"
app_icon = "octicon octicon-repo-pull"
app_color = "grey"
app_email = "hello@frappe.io"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/odoo_to_erpnext/css/odoo_to_erpnext.css"
# app_include_js = "/assets/odoo_to_erpnext/js/odoo_to_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/odoo_to_erpnext/css/odoo_to_erpnext.css"
# web_include_js = "/assets/odoo_to_erpnext/js/odoo_to_erpnext.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "odoo_to_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "odoo_to_erpnext.install.before_install"
# after_install = "odoo_to_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "odoo_to_erpnext.notifications.get_notification_config"

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

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"odoo_to_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"odoo_to_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"odoo_to_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"odoo_to_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"odoo_to_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "odoo_to_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "odoo_to_erpnext.event.get_events"
# }

