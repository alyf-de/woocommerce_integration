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


def log_woocommerce_error(order: dict):
	error_message = (
		frappe.get_traceback()
		+ "\n\n Request Data: \n"
		+ frappe.as_json(order)
	)
	frappe.log_error(
		title=_("WooCommerce Error"), message=error_message,
	)
