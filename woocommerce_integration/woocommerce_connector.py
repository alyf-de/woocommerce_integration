from woocommerce import API as WCAPI

from woocommerce_integration.general_utils import (
    build_filter_string,
    log_woocommerce_error,
)


class WooCommerceConnector:
    def __init__(self, setup: dict):
        self.settings = setup
        self.url = self.settings.url
        self.consumer_key = self.settings.consumer_key
        self.consumer_secret = self.settings.consumer_secret
        self.woocommerce = WCAPI(
            url=self.url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            wc_api=True,
            verify_ssl=self.settings.verify_ssl,
            version="wc/v3",
            timeout=1000,
        )

    def get_products(self, filters: dict | None = None):
        filter_string = build_filter_string(filters)
        try:
            response = self.woocommerce.get(
                f'products{f"?{filter_string}" if filter_string else ""}'
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            log_woocommerce_error(response)
            raise

    def get_product(self, id: str):
        try:
            response = self.woocommerce.get(f"products/{id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            log_woocommerce_error(response)
            raise

    def create_product(self, product_data: dict):
        try:
            response = self.woocommerce.post("products", product_data)
            response.raise_for_status()
            return response.json()
        except Exception:
            log_woocommerce_error(response)
            raise

    def update_product(self, id: str, product_data: dict):
        try:
            response = self.woocommerce.put(f"products/{id}", product_data)
            response.raise_for_status()
            return response.json()
        except Exception:
            log_woocommerce_error(response)
            raise

    def batch_update_products(self, product_data: dict):
        try:
            response = self.woocommerce.post("products/batch", product_data)
            response.raise_for_status()
            return response.json()
        except Exception:
            log_woocommerce_error(response)
            raise

    def delete_product(self, id: str):
        try:
            response = self.woocommerce.delete(f"products/{id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            log_woocommerce_error(response)
            raise
