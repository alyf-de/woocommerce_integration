# Copyright (c) 2024, ALYF GmbH and contributors
# For license information, please see license.txt
from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.model.document import Document

from woocommerce_integration.webhooks import ACTION_MAP
from woocommerce_integration.general_utils import get_woocommerce_setup

STOCK_UPDATE_METHODS = frappe._dict(
	event_based="On Stock Update",
	time_based="In Certain Time Intervals"
)


class WooCommerceSetup(Document):
	def onload(self):
		series = frappe.get_meta("Sales Order").get_options("naming_series") or "SO-WOO-"
		self.set_onload("sales_order_series", series)

	def before_validate(self):
		# Use "Nos" only if the default UOM is not set
		self.default_uom = self.default_uom if self.default_uom else "Nos"
		self.set_webhook_urls()

	def validate(self):
		self.validate_interval()

	def on_update(self):
		self.create_scheduled_job()

	def validate_interval(self):
		if (
			self.enable_stock_sync
			and self.stock_update_method == STOCK_UPDATE_METHODS.time_based
			and self.interval_in_minutes > 60
		):
			frappe.throw(
				_("Interval in minutes cannot be greater than 60 minutes.")
			)

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

	def create_scheduled_job(self):
		"""Create a scheduled job for the stock sync."""
		if not self.enable_stock_sync or (
			self.stock_update_method != STOCK_UPDATE_METHODS.time_based
		) or not self.interval_in_minutes:
			if self.scheduled_job:
				# Disable the scheduled job
				self.disable_job(disabled=True)

			return

		if not self.has_value_changed("interval_in_minutes"):
			# No change in interval, no need to create/update a scheduled job
			# Just enable the job if it was disabled
			self.disable_job(disabled=False)
			return

		if self.scheduled_job:
			job = frappe.get_doc("Scheduled Job Type", self.scheduled_job)
			job.cron_format = f"0/{self.interval_in_minutes} * * * *"
			job.stopped = 0
		else:
			job = frappe.get_doc(
				dict(
					doctype="Scheduled Job Type",
					method="woocommerce_integration.stock_sync_utils.batch_update_stock",
					frequency="Cron",
					cron_format=f"0/{self.interval_in_minutes} * * * *",
				)
			)

		job.save()
		self.db_set("scheduled_job", job.name)

	def disable_job(self, disabled: bool):
		"""Enable or disable the scheduled job."""
		job = frappe.get_doc("Scheduled Job Type", self.scheduled_job)
		job.stopped = disabled
		job.save()
