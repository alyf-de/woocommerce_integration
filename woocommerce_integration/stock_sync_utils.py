import frappe

from woocommerce_integration.general_utils import get_woocommerce_setup
from woocommerce_integration.woocommerce_connector import WooCommerceConnector
from woocommerce_integration.woocommerce.doctype.woocommerce_setup.woocommerce_setup import (
	STOCK_UPDATE_METHODS,
)


def batch_update_stock():
	"""
	Flow: From ERPNext to WooCommerce.
	Called by the scheduler. Batch update items from all recent stock updates.
	"""
	setup = get_woocommerce_setup()
	if not setup.enable_stock_sync or (
		setup.stock_update_method != STOCK_UPDATE_METHODS.time_based
	):
		return

	# Get all recent Bins
	data = {"update": []}
	for row in frappe.get_all(
		"Bin",
		filters={
			"warehouse": setup.warehouse,
			"modified": (">=", setup.last_stock_sync),
		},
		fields=["item_code", "actual_qty"],
	):
		if product_id := frappe.db.get_value(
			"Item", row.item_code, "woocomm_product_id"
		):
			data["update"].append(
				{
					"id": product_id,
					"stock_quantity": row.actual_qty,
					"manage_stock": True
				}
			)

	# Update stock in WooCommerce
	if data["update"]:
		connector = WooCommerceConnector(setup)
		connector.batch_update_products(data)
		frappe.db.set_value(
			"WooCommerce Setup", None, "last_stock_sync", frappe.utils.now()
		)


def update_stock_for_item(sle_doc: dict, event: str):
	"""
	Flow: From ERPNext to WooCommerce.
	Called on SLE insert. Update item stock from SLE Doc.
	"""
	setup = get_woocommerce_setup()
	if not setup.enable_stock_sync or (
		setup.stock_update_method != STOCK_UPDATE_METHODS.event_based
	):
		return

	if sle_doc.warehouse != setup.warehouse:
		return

	product_id = frappe.db.get_value("Item", sle_doc.item_code, "woocomm_product_id")
	if not product_id:
		return

	# Update stock in WooCommerce
	connector = WooCommerceConnector(setup)
	connector.update_product(
		product_id,
		{
			"stock_quantity": sle_doc.qty_after_transaction,
			"manage_stock": True
		},
	)
