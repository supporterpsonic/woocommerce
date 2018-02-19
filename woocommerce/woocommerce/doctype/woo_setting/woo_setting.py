# -*- coding: utf-8 -*-
# Copyright (c) 2017, WooCommerce and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json

from woocommerce import API

class WooSetting(Document):
	pass


@frappe.whitelist()
def get_data_woo_setting():

	url_woo = frappe.db.sql("""
		SELECT
		ws.`name`,
		ws.`url`,
		ws.`consumer_key`,
		ws.`consumer_secret`,
		ws.`warehouse_item`,
		ws.`price_list_item`
		FROM `tabWoo Setting` ws
	""", as_list=1)

	if url_woo :
		return url_woo
	else :
		return

@frappe.whitelist()
def connect_woo_api_v2(url, consumer_key, consumer_secret):
	
	wcapi = API(
	    url = url,
	    consumer_key = consumer_key,
	    consumer_secret = consumer_secret,
	    wp_api=True,
	    version="wc/v1"
	)

	return wcapi

# ================================ PRODUCT ========================================== #

@frappe.whitelist()
def get_id_by_sku(sku, url, consumer_key, consumer_secret):

	wcapi = connect_woo_api_v2(url, consumer_key, consumer_secret)
	data_product = wcapi.get("products").json()

	product_id = "tidak_ada"
	if data_product :
		for x in data_product :
			if x["sku"] == sku :
				product_id = x["id"]
				break

	# frappe.throw(str(product_id))

	return product_id


@frappe.whitelist()
def membuat_atau_update_item_baru(doc, method):

	# ambil data woo setting
	get_woo_setting = get_data_woo_setting()
	if get_woo_setting :
		for i in get_woo_setting :

			# connect ke woocommerce sesuai dengan woo_setting
			wcapi = connect_woo_api_v2(str(i[1]), str(i[2]), str(i[3]))

			# ambil product_id dari woocommerce berdasarkan item code / sku
			product_id = str(get_id_by_sku(doc.item_code, str(i[1]), str(i[2]), str(i[3])))

			if product_id == "tidak_ada" :
				if doc.is_sales_item == 1 :
					data = {
						"name": doc.item_name,
					    "type": "simple",
					    "description": doc.description,
					    "short_description": doc.description,
					    "sku": doc.item_code,
				  		"manage_stock": True
					}
					wcapi.post("products", data)
			else :
				if doc.disabled == 0 :
					if doc.is_sales_item == 1 :
						data = {
							"name": doc.item_name,
						    "type": "simple",
						    "description": doc.description,
						    "short_description": doc.description,
						    "sku": doc.item_code,
					  		"manage_stock": True,
					  		"status": "publish",
						}
						wcapi.put("products/"+str(product_id), data)
				elif doc.disabled == 1 :
					if doc.is_sales_item == 1 :
						data = {
							"name": doc.item_name,
						    "type": "simple",
						    "description": doc.description,
						    "short_description": doc.description,
						    "sku": doc.item_code,
					  		"manage_stock": True,
					  		"status": "pending",
						}
						wcapi.put("products/"+str(product_id), data)
						
			

@frappe.whitelist()
def hapus_item_woocommerce(doc, method):

	# ambil data woo setting
	get_woo_setting = get_data_woo_setting()
	if get_woo_setting :
		for i in get_woo_setting :

			# connect ke woocommerce sesuai dengan woo_setting
			wcapi = connect_woo_api_v2(str(i[1]), str(i[2]), str(i[3]))

			# ambil product_id dari woocommerce berdasarkan item code / sku
			product_id = str(get_id_by_sku(doc.item_code, str(i[1]), str(i[2]), str(i[3])))

			count = 0
			if product_id == "tidak_ada" :
				count = 0
			else :
				wcapi.delete("products/"+product_id+"?force=true")
				frappe.msgprint("Item juga sudah terhapus dari dalam WooCommerce "+str(i[0]))


@frappe.whitelist()
def add_edit_item_price(doc, method):

	# ambil data woo setting
	url_woo = frappe.db.sql("""
		SELECT
		ws.`name`,
		ws.`url`,
		ws.`consumer_key`,
		ws.`consumer_secret`,
		ws.`warehouse_item`,
		ws.`price_list_item`
		FROM `tabWoo Setting` ws
		WHERE ws.`price_list_item` = "{0}"
	""".format(doc.price_list), as_list=1)

	if url_woo :

		for i in url_woo :

			# connect ke woocommerce sesuai dengan woo_setting
			wcapi = connect_woo_api_v2(str(i[1]), str(i[2]), str(i[3]))

			# frappe.throw(" URL : "+str(i[1]) + " KEY : " + str(i[2]) + " SECRET : " + str(i[3]))

			# ambil product_id dari woocommerce berdasarkan item code / sku
			product_id = str(get_id_by_sku(doc.item_code, str(i[1]), str(i[2]), str(i[3])))

			# frappe.throw(str(product_id))
			# frappe.throw(str(wcapi))

			count = 0
			if product_id == "tidak_ada" :
				count = 0
			else :
				data = {
					"price": str(doc.price_list_rate),
					"regular_price": str(doc.price_list_rate),
				}
				# frappe.throw(str(data))
				wcapi.put("products/"+str(product_id), data)
				

@frappe.whitelist()
def delete_item_price(doc, method):

	# ambil data woo setting
	url_woo = frappe.db.sql("""
		SELECT
		ws.`name`,
		ws.`url`,
		ws.`consumer_key`,
		ws.`consumer_secret`,
		ws.`warehouse_item`,
		ws.`price_list_item`
		FROM `tabWoo Setting` ws
		WHERE ws.`price_list_item` = "{0}"
	""".format(doc.price_list), as_list=1)

	if url_woo :

		for i in url_woo :

			# connect ke woocommerce sesuai dengan woo_setting
			wcapi = connect_woo_api_v2(str(i[1]), str(i[2]), str(i[3]))

			# ambil product_id dari woocommerce berdasarkan item code / sku
			product_id = str(get_id_by_sku(doc.item_code, str(i[1]), str(i[2]), str(i[3])))

			count = 0
			if product_id == "tidak_ada" :
				count = 0
			else :
				data = {
					"price": str("0"),
					"regular_price": str("0"),
				}
				wcapi.put("products/"+str(product_id), data)

# ================================= END PRODUCT ========================================== #

# ================================== STOCK PRODUCT ========================================== #


# submit stock entry
@frappe.whitelist()
def submit_cancel_document_stock_entry(doc, method):

	if doc.purpose == "Material Receipt" :

		for i in doc.items :

			url_woo = frappe.db.sql("""
				SELECT
				ws.`name`,
				ws.`url`,
				ws.`consumer_key`,
				ws.`consumer_secret`,
				ws.`warehouse_item`,
				ws.`price_list_item`
				FROM `tabWoo Setting` ws
				WHERE ws.`warehouse_item` = "{0}"
			""".format(i.t_warehouse), as_list=1)

			if url_woo :

				for x in url_woo :

					get_data_bin = frappe.db.sql("""
						SELECT
						b.`item_code`,
						b.`warehouse`,
						b.`actual_qty`
						FROM `tabBin` b
						WHERE b.`item_code` = "{0}"
						AND b.`warehouse` = "{1}"
					""".format(i.item_code, i.t_warehouse), as_list=1)

					if get_data_bin :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": float(get_data_bin[0][2])
						}
						wcapi.put("products/"+str(product_id), data)

					else :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": 0
						}
						wcapi.put("products/"+str(product_id), data)


	elif doc.purpose == "Material Issue" :

		for i in doc.items :

			url_woo = frappe.db.sql("""
				SELECT
				ws.`name`,
				ws.`url`,
				ws.`consumer_key`,
				ws.`consumer_secret`,
				ws.`warehouse_item`,
				ws.`price_list_item`
				FROM `tabWoo Setting` ws
				WHERE ws.`warehouse_item` = "{0}"
			""".format(i.s_warehouse), as_list=1)

			if url_woo :

				for x in url_woo :

					get_data_bin = frappe.db.sql("""
						SELECT
						b.`item_code`,
						b.`warehouse`,
						b.`actual_qty`
						FROM `tabBin` b
						WHERE b.`item_code` = "{0}"
						AND b.`warehouse` = "{1}"
					""".format(i.item_code, i.s_warehouse), as_list=1)

					if get_data_bin :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": float(get_data_bin[0][2])
						}
						wcapi.put("products/"+str(product_id), data)

					else :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": 0
						}
						wcapi.put("products/"+str(product_id), data)


	elif doc.purpose == "Material Transfer" :

		for i in doc.items :

			# from warehouse
			url_woo_t = frappe.db.sql("""
				SELECT
				ws.`name`,
				ws.`url`,
				ws.`consumer_key`,
				ws.`consumer_secret`,
				ws.`warehouse_item`,
				ws.`price_list_item`
				FROM `tabWoo Setting` ws
				WHERE ws.`warehouse_item` = "{0}"
			""".format(i.t_warehouse), as_list=1)

			if url_woo_t :

				for x in url_woo_t :

					get_data_bin_t = frappe.db.sql("""
						SELECT
						b.`item_code`,
						b.`warehouse`,
						b.`actual_qty`
						FROM `tabBin` b
						WHERE b.`item_code` = "{0}"
						AND b.`warehouse` = "{1}"
					""".format(i.item_code, i.t_warehouse), as_list=1)

					if get_data_bin_t :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": float(get_data_bin_t[0][2])
						}
						wcapi.put("products/"+str(product_id), data)

					else :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": 0
						}
						wcapi.put("products/"+str(product_id), data)


			# source warehouse
			url_woo_s = frappe.db.sql("""
				SELECT
				ws.`name`,
				ws.`url`,
				ws.`consumer_key`,
				ws.`consumer_secret`,
				ws.`warehouse_item`,
				ws.`price_list_item`
				FROM `tabWoo Setting` ws
				WHERE ws.`warehouse_item` = "{0}"
			""".format(i.s_warehouse), as_list=1)

			if url_woo_s :

				for x in url_woo_t :

					get_data_bin_s = frappe.db.sql("""
						SELECT
						b.`item_code`,
						b.`warehouse`,
						b.`actual_qty`
						FROM `tabBin` b
						WHERE b.`item_code` = "{0}"
						AND b.`warehouse` = "{1}"
					""".format(i.item_code, i.s_warehouse), as_list=1)

					if get_data_bin_s :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": float(get_data_bin_s[0][2])
						}
						wcapi.put("products/"+str(product_id), data)

					else :
						# connect ke woocommerce sesuai dengan woo_setting
						wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
						# ambil product_id dari woocommerce berdasarkan item code / sku
						product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
						data = {
							"stock_quantity": 0
						}
						wcapi.put("products/"+str(product_id), data)



# submit purchase receipt
@frappe.whitelist()
def submit_cancel_document_purchase_receipt(doc, method):

	for i in doc.items :

		url_woo = frappe.db.sql("""
			SELECT
			ws.`name`,
			ws.`url`,
			ws.`consumer_key`,
			ws.`consumer_secret`,
			ws.`warehouse_item`,
			ws.`price_list_item`
			FROM `tabWoo Setting` ws
			WHERE ws.`warehouse_item` = "{0}"
		""".format(i.warehouse), as_list=1)

		if url_woo :

			for x in url_woo :

				get_data_bin = frappe.db.sql("""
					SELECT
					b.`item_code`,
					b.`warehouse`,
					b.`actual_qty`
					FROM `tabBin` b
					WHERE b.`item_code` = "{0}"
					AND b.`warehouse` = "{1}"
				""".format(i.item_code, i.warehouse), as_list=1)

				if get_data_bin :
					# connect ke woocommerce sesuai dengan woo_setting
					wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
					# ambil product_id dari woocommerce berdasarkan item code / sku
					product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
					data = {
						"stock_quantity": float(get_data_bin[0][2])
					}
					wcapi.put("products/"+str(product_id), data)

				else :
					# connect ke woocommerce sesuai dengan woo_setting
					wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
					# ambil product_id dari woocommerce berdasarkan item code / sku
					product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
					data = {
						"stock_quantity": 0
					}
					wcapi.put("products/"+str(product_id), data)


# submit stock reconcilliation
@frappe.whitelist()
def submit_cancel_document_stock_reconcilliation(doc, method):

	for i in doc.items :

		url_woo = frappe.db.sql("""
			SELECT
			ws.`name`,
			ws.`url`,
			ws.`consumer_key`,
			ws.`consumer_secret`,
			ws.`warehouse_item`,
			ws.`price_list_item`
			FROM `tabWoo Setting` ws
			WHERE ws.`warehouse_item` = "{0}"
		""".format(i.warehouse), as_list=1)

		if url_woo :

			for x in url_woo :

				get_data_bin = frappe.db.sql("""
					SELECT
					b.`item_code`,
					b.`warehouse`,
					b.`actual_qty`
					FROM `tabBin` b
					WHERE b.`item_code` = "{0}"
					AND b.`warehouse` = "{1}"
				""".format(i.item_code, i.warehouse), as_list=1)

				if get_data_bin :
					# connect ke woocommerce sesuai dengan woo_setting
					wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
					# ambil product_id dari woocommerce berdasarkan item code / sku
					product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
					data = {
						"stock_quantity": float(get_data_bin[0][2])
					}
					wcapi.put("products/"+str(product_id), data)

				else :
					# connect ke woocommerce sesuai dengan woo_setting
					wcapi = connect_woo_api_v2(str(x[1]), str(x[2]), str(x[3]))
					# ambil product_id dari woocommerce berdasarkan item code / sku
					product_id = str(get_id_by_sku(i.item_code, str(x[1]), str(x[2]), str(x[3])))
					data = {
						"stock_quantity": 0
					}
					wcapi.put("products/"+str(product_id), data)



# ================================== END STOCK PRODUCT ========================================== #