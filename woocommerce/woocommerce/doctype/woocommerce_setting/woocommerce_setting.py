# -*- coding: utf-8 -*-
# Copyright (c) 2017, WooCommerce and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

# from woocommerce.woocommerce.doctype.woocommerce_setting.woocommerce import API
# from woocommerce import API

class WooCommerceSetting(Document):
	pass


# @frappe.whitelist()
# def connect_woo_api():

# 	single = frappe.db.sql("""
# 		SELECT
# 		s.`field`,
# 		s.`value`
# 		FROM `tabSingles` s
# 		WHERE s.`doctype` = "WooCommerce Setting"
# 		AND (s.`field` = "consumer_key" OR s.`field` = "consumer_secret" OR s.`field` = "url" OR s.`field` = "price_list_item" OR s.`field` = "warehouse_item")

# 		ORDER BY s.`field`
# 	""", as_list=1)


# 	url = ""
# 	consumer_key = ""
# 	consumer_secret = ""
# 	price_list_item = ""
# 	warehouse_item = ""


# 	for i in single :
# 		if i[0] == "consumer_key" :
# 			consumer_key = i[1]
# 		elif i[0] == "consumer_secret" :
# 			consumer_secret = i[1]
# 		elif i[0] == "url" :
# 			url = i[1]
# 		elif i[0] == "price_list_item" :
# 			price_list_item = i[1]
# 		elif i[0] == "warehouse_item" :
# 			warehouse_item = i[1]

# 	wcapi = API(
# 	    url = url,
# 	    consumer_key = consumer_key,
# 	    consumer_secret = consumer_secret,
# 	    wp_api=True,
# 	    version="wc/v1"
# 	)

# 	return wcapi


# @frappe.whitelist()
# def membuat_item_baru(doc, method):

# 	wcapi = connect_woo_api()

# 	data = {
# 	    "name": doc.item_name,
# 	    "type": "simple",
# 	    "regular_price": "10.000",
# 	    "description": doc.description,
# 	    "short_description": doc.description,
# 	    "sku": doc.item_code,
# 	}

# 	wcapi.post("products", data)


