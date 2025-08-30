from datetime import datetime

import frappe
from frappe import _
from frappe.utils import cstr, flt

from woocommerce_integration.general_utils import get_woocommerce_setup


def create_sales_order(order_data: dict, setup: dict):
    """Create a sales order with its dependencies."""
    if not setup:
        setup = get_woocommerce_setup()

    try:
        customer, billing_address, shipping_address = create_update_customer(order_data)
        create_order(order_data, setup, customer.name, billing_address, shipping_address)
    except Exception:
        frappe.log_error(
            message=frappe.get_traceback(),
            title=_("WooCommerce Error: Creation of Sales Order"),
        )
        raise


def create_update_customer(order_data: dict):
    """Create or update a customer based on the order data."""
    billing_data = order_data.get("billing")
    customer_id = order_data.get("customer_id")
    customer_name = billing_data.get("first_name") + " " + billing_data.get("last_name")

    # Customer could have been created manually which may differ in naming
    # always check woocomm_customer_id
    if erp_customer := frappe.db.exists(
        "Customer", {"woocomm_customer_id": customer_id}
    ):
        customer = frappe.get_doc("Customer", erp_customer)
    else:
        customer = frappe.new_doc("Customer")
        customer.name = customer_id

    customer.customer_name = customer_name
    customer.woocomm_customer_id = customer_id
    customer.flags.ignore_mandatory = True
    customer.save()

    # Create address/contact if does not exist
    billing_address = create_address(billing_data, customer, "Billing")
    shipping_address = create_address(order_data.get("shipping"), customer, "Shipping")

    create_contact(billing_data, customer)

    return customer, billing_address, shipping_address


def get_uom(sku: str | None, default_uom: str):
    """Get the SKU from WooCommerce or the default UOM for the item."""
    if sku and not frappe.db.exists("UOM", sku):
        frappe.get_doc({"doctype": "UOM", "uom_name": sku}).save()

    return sku or (default_uom or "Nos")


def create_address(raw_data: dict, customer: dict, address_type: str):
    """Create an address for the customer if it does not exist."""
    if address := frappe.db.exists(
        "Address",
        {
            "pincode": raw_data.get("postcode"),
            "address_line1": raw_data.get("address_1", "Not Provided"),
            "woocomm_customer_id": customer.woocomm_customer_id,
            "address_type": address_type,
        },
    ):
        return address

    address = frappe.new_doc("Address")
    address.address_title = customer.get("customer_name")
    address.address_line1 = raw_data.get("address_1", "Not Provided")
    address.address_line2 = raw_data.get("address_2")
    address.city = raw_data.get("city", "Not Provided")
    address.woocomm_customer_id = customer.woocomm_customer_id
    address.address_type = address_type
    address.state = raw_data.get("state")
    address.pincode = raw_data.get("postcode")
    address.phone = raw_data.get("phone")
    address.email_id = raw_data.get("email")

    if country := raw_data.get("country"):
        address.country = frappe.db.get_value("Country", {"code": country.lower()})
    else:
        address.country = frappe.get_system_settings("country")

    address.append("links", {"link_doctype": "Customer", "link_name": customer.name})
    address.flags.ignore_mandatory = True
    address.save()
    return address.name


def create_contact(data: dict, customer: str):
    email = data.get("email")
    phone = data.get("phone")
    if not email and not phone:
        return

    if frappe.db.exists(
        "Contact",
        {
            "email_id": email,
            "woocomm_customer_id": customer.woocomm_customer_id,
        },
    ):
        return

    contact = frappe.new_doc("Contact")
    contact.first_name = data.get("first_name")
    contact.last_name = data.get("last_name")
    contact.email_id = email
    contact.woocomm_customer_id = customer.woocomm_customer_id
    contact.is_primary_contact = 1
    contact.is_billing_contact = 1

    if phone:
        contact.add_phone(phone, is_primary_mobile_no=1, is_primary_phone=1)

    if email:
        contact.add_email(email, is_primary=1)

    contact.append("links", {"link_doctype": "Customer", "link_name": customer.name})
    contact.flags.ignore_mandatory = True
    contact.save()


def create_order(order: dict, woocommerce_setup: dict, customer: str, billing_address=None, shipping_address=None):
    """Create a sales order based on the order data."""
    sales_order = frappe.new_doc("Sales Order")
    sales_order.customer = customer
    sales_order.company = woocommerce_setup.default_company
    sales_order.po_no = sales_order.woocomm_order_id = order.get("id")
    sales_order.naming_series = woocommerce_setup.sales_order_series

    created_date = datetime.fromisoformat(order.get("date_created")).date()
    sales_order.transaction_date = created_date
    sales_order.delivery_date = frappe.utils.add_days(
        created_date, woocommerce_setup.delivery_after or 7
    )

    sales_order.customer_address = billing_address
    sales_order.shipping_address_name = shipping_address

    add_items_to_sales_order(order, sales_order, woocommerce_setup)

    sales_order.flags.ignore_permissions = True
    sales_order.run_method("set_missing_values")
    sales_order.run_method("calculate_taxes_and_totals")

    sales_order.flags.ignore_mandatory = True
    sales_order.insert()
    sales_order.submit()


def add_items_to_sales_order(order: dict, sales_order: dict, setup: dict):
    """Set the items in the sales order with taxes based on the order data."""
    for line_item in order.get("line_items") or []:
        item = get_item(line_item, setup)
        sales_order.append(
            "items",
            {
                "item_code": item.name,
                "item_name": item.item_name,
                "description": item.description,
                "delivery_date": sales_order.delivery_date,
                "uom": get_uom(line_item.get("sku"), setup.default_uom),
                "qty": line_item.get("quantity"),
                "rate": line_item.get("price"),
                "warehouse": setup.default_warehouse,
            },
        )
    


def get_item(item_data: dict, setup: dict) -> dict:
    """Get item document or create it if it does not exist."""
    woo_com_id = item_data["product_id"]
    if erp_item := frappe.db.exists("Item", {"woocomm_product_id": woo_com_id}):
        return frappe.db.get_values(
            "Item", erp_item, ["name", "item_name", "description"], as_dict=True
        )[0]

    return create_item(item_data, woo_com_id, setup)


def create_item(item_data: dict, woo_com_id: str, setup: dict):
    """Create an item based on the item data."""
    item = frappe.new_doc("Item")
    item.item_code = cstr(woo_com_id)
    item.item_name = item_data.get("name")
    item.stock_uom = get_uom(item_data.get("sku"), setup.default_uom)
    item.item_group = "WooCommerce Products"
    item.image = (item_data.get("image") or {}).get("src")
    item.woocomm_product_id = cstr(woo_com_id)
    item.flags.ignore_mandatory = True
    item.save()

    return item
