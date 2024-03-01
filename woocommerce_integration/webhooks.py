import frappe

from woocommerce_integration.general_utils import (
	log_woocommerce_error,
	process_request_data,
	verify_webhook,
)
from woocommerce_integration.order_creation_utils import create_sales_order

ACTION_MAP = {
	"Order created": "create_order",
	"Order updated": "update_order",
	"Order deleted": "delete_order",
	"Customer updated": "update_customer",
}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_order():
	verify_webhook()
	skip, order = process_request_data()
	if skip:
		return "success"

	try:
		create_sales_order(order)
	except Exception:
		log_woocommerce_error(order)
		raise


@frappe.whitelist(allow_guest=True)
def update_order():
	pass


@frappe.whitelist(allow_guest=True)
def delete_order():
	"""Cancel a Sales Order in ERPNext when an order is deleted in WooCommerce."""
	pass


@frappe.whitelist(allow_guest=True)
def update_customer():
	pass
