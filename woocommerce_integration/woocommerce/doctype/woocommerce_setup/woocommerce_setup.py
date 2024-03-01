# Copyright (c) 2024, ALYF GmbH and contributors
# For license information, please see license.txt
from urllib.parse import urlparse

import frappe
from frappe.model.document import Document

from woocommerce_integration.webhooks import ACTION_MAP
from woocommerce_integration.general_utils import get_woocommerce_setup


class WooCommerceSetup(Document):
	def onload(self):
		series = frappe.get_meta("Sales Order").get_options("naming_series") or "SO-WOO-"
		self.set_onload("sales_order_series", series)

	def before_validate(self):
		# Use "Nos" only if the default UOM is not set
		self.default_uom = self.default_uom if self.default_uom else "Nos"
		self.set_webhook_urls()

	@frappe.whitelist()
	def generate_secret(self):
		woocommerce_setup = get_woocommerce_setup()
		woocommerce_setup.webhook_secret = frappe.generate_hash()
		woocommerce_setup.save()

	def set_webhook_urls(self):
		"""Set the webhook URLs for the WooCommerce actions."""
		if self.webhook_endpoints:
			return

		try:
			url = frappe.request.url
		except Exception:
			url = "http://localhost:8000"

		server_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))
		path_to_webhooks = "/api/method/woocommerce_integration.webhooks"
		endpoints = [
			f"{action}: {server_url + path_to_webhooks + '.' + method}"
			for action, method in ACTION_MAP.items()
		]

		self.webhook_endpoints = "\n".join(endpoints)
