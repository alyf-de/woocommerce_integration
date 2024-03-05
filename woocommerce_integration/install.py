import frappe
from click import echo
from frappe.custom.doctype.custom_field.custom_field import (
	create_custom_fields,
)


def after_install():
	echo("Creating custom fields...")
	make_custom_fields()

	echo("Inserting dependent data...")
	make_woocommerce_records()


def after_uninstall():
	echo("Deleting custom fields...")
	for key, value in frappe.get_hooks("woocomm_custom_fields", {}).items():
		if isinstance(key, tuple):
			for doctype in key:
				delete_custom_fields(doctype, value)
		else:
			delete_custom_fields(key, value)


def delete_custom_fields(doctype, fields):
	frappe.db.delete(
		"Custom Field",
		{
			"fieldname": ("in", [field["fieldname"] for field in fields]),
			"dt": doctype,
		},
	)

	frappe.clear_cache(doctype=doctype)


def make_custom_fields():
	for key, value in frappe.get_hooks("woocomm_custom_fields", {}).items():
		if isinstance(key, tuple):
			for doctype in key:
				create_custom_fields({doctype: value}, ignore_validate=True)
		else:
			create_custom_fields({key: value}, ignore_validate=True)


def make_woocommerce_records():
	"""Create records for WooCommerce setup."""
	groups = ["All Item Groups", "WooCommerce Products"]
	for group in groups:
		if frappe.db.exists("Item Group", group):
			continue

		frappe.get_doc(
			{
				"doctype": "Item Group",
				"item_group_name": group,
				"parent_item_group": (
					None if group == "All Item Groups" else "All Item Groups"
				),
			}
		).insert(ignore_permissions=True)
