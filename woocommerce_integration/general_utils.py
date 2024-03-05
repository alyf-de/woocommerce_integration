import base64
import hashlib
import json
from hmac import new as HMAC
from typing import Tuple, Optional

import frappe
from frappe import _


def get_woocommerce_setup():
	"""Get the WooCommerce Setup document."""
	return frappe.get_single("WooCommerce Setup")


def verify_webhook():
	woocommerce_setup = get_woocommerce_setup()
	sig = base64.b64encode(
		HMAC(
			woocommerce_setup.webhook_secret.encode("utf8"),
			frappe.request.data,
			hashlib.sha256
		).digest()
	)

	if not frappe.request.data:
		frappe.log_error(message=_("No Webhook Data"))
		frappe.throw(_("No Webhook Data"), exc=frappe.ValidationError)

	if (
		frappe.request.data
		and sig != frappe.get_request_header("X-Wc-Webhook-Signature", "").encode()
	):
		frappe.log_error(message=_("Unverified Webhook Data"))
		frappe.throw(_("Unverified Webhook Data"), exc=frappe.AuthenticationError)

	frappe.set_user(woocommerce_setup.default_user)


def process_request_data() -> Tuple[bool, Optional[dict]]:
	"""
	Process the request data from WooCommerce.
	Returns a tuple with a 'skip' boolean and an 'order' dictionary.
	"""
	if isinstance(order := frappe.request.data, str):
		return (True, None) if "webhook_id" in order else (False, json.loads(order))

	return False, order


def build_filter_string(filters: dict) -> str:
	"""
	Build a filter string from a dict for the WooCommerce API.
	"""
	if not filters:
		return ""

	return "&".join([
		f"{key}={value}" for key, value in filters.items()
	])


def log_woocommerce_error(response: dict):
	log_response = (
		frappe.as_json(response)
		if isinstance(response, (dict, list,))
		else response
	) if response else "No Response Data"

	error_message = (
		frappe.get_traceback()
		+ "\n\n Request Data: \n"
		+ log_response
	)
	frappe.log_error(
		title=_("WooCommerce Error"), message=error_message,
	)
