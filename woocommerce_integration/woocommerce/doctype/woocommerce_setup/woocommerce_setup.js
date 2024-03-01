// Copyright (c) 2024, ALYF GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('WooCommerce Setup', {
	onload: function(frm) {
		if (frm.doc.__onload && frm.doc.__onload.sales_order_series) {
			set_field_options('sales_order_series', frm.doc.__onload.sales_order_series);
		}
	},

	refresh: function(frm) {
		frm.events.add_button_generate_secret(frm);
	},

	add_button_generate_secret(frm) {
		frm.add_custom_button(__('Generate Secret'), () => {
			frappe.confirm(
				__('This will require resetting the webhook secret in your WooCommerce instance.'),
				() => {
					frm.call("generate_secret").then(() => frm.reload_doc());
				}
			);
		});
	},
});
