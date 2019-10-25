import json
import logging

import pytest

from services.local_pay_co_data_service import LocalPayCoDataService
from tests.test_utils import TestUtils


class TestPayCoDataService:
    _logger = logging.getLogger(__name__)

    @pytest.mark.parametrize("product_id,expected_product_id",
                             [(1, 'product_1'),
                              (2, 'product_2'),
                              (0, None)
                              ])
    def test_find_product(self, product_id, expected_product_id):
        service = LocalPayCoDataService('resources/data')
        product = service.find_product(product_id)
        if expected_product_id is None:
            assert product is None
        else:
            assert product['id'] == expected_product_id

    @pytest.mark.parametrize("customer_id,expected_customer_id",
                             [(1, 'customer_1'),
                              (2, 'customer_2'),
                              (0, None)
                              ])
    def test_find_customer(self, customer_id, expected_customer_id):
        service = LocalPayCoDataService('resources/data')
        customer = service.find_customer(customer_id)
        if expected_customer_id is None:
            assert customer is None
        else:
            assert customer['id'] == expected_customer_id

    def test_process_usage_with_valid_product_plan_and_subscription(self):
        service = LocalPayCoDataService('resources/data')
        usage_data = service.process_usage(1)
        expected_usage_data = {
            "allowsApiOverage": True,
            "details": {
                "apiCalls": "1000",
                "requestSize": "1KB",
                "storage": "500MB"
            },
            "status": "active",
            "subscriptionStartsAt": 1567099267,
            "subscriptionEndsAt": 1569691245
        }
        self._logger.info(json.dumps(usage_data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(usage_data, expected_usage_data)

    def test_process_usage_with_valid_product_plan_with_customer_override(self):
        service = LocalPayCoDataService('tests/resources/usage_data/valid_product_plan_with_customer_override')
        usage_data = service.process_usage(1)
        expected_usage_data = {
            "allowsApiOverage": True,
            "details": {
                "apiCalls": "5000",
                "storage": "600MB",
                "requestSize": "2KB"
            },
            "status": "active",
            "subscriptionStartsAt": 1567099267,
            "subscriptionEndsAt": 1569691245
        }
        self._logger.info(json.dumps(usage_data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(usage_data, expected_usage_data)

    def test_process_usage_with_mix_subscription_with_valid_inactive_subscription(self):
        service = LocalPayCoDataService('tests/resources/usage_data/mix_subscription_with_valid_inactive_subscription')
        usage_data = service.process_usage(1)
        expected_usage_data = {
            "allowsApiOverage": True,
            "details": {
                "apiCalls": "1000",
                "requestSize": "1KB",
                "storage": "500MB"
            },
            "status": "inactive",
            "subscriptionStartsAt": 1567099267,
            "subscriptionEndsAt": 1569691245
        }
        self._logger.info(json.dumps(usage_data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(usage_data, expected_usage_data)

    def test_process_usage_with_non_metered_trialing_subscription(self):
        service = LocalPayCoDataService('resources/data')
        usage_data = service.process_usage(2)
        expected_usage_data = {
            "allowsApiOverage": False,
            "details": {
                "apiCalls": "1000",
                "requestSize": "1KB",
                "storage": "500MB"
            },
            "status": "active",
            "subscriptionStartsAt": 1567099447,
            "subscriptionEndsAt": 1569691447
        }
        self._logger.info(json.dumps(usage_data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(usage_data, expected_usage_data)

    def test_process_usage_mix_subscription_with_valid_inactive_and_active_subscription(self):
        service = LocalPayCoDataService(
            'tests/resources/usage_data/mix_subscription_with_valid_inactive_and_active_subscription')
        usage_data = service.process_usage(2)
        expected_usage_data = {
            "allowsApiOverage": True,
            "details": {
                "apiCalls": "2000",
                "requestSize": "1KB",
                "storage": "500MB"
            },
            "status": "active",
            "subscriptionStartsAt": 1567099267,
            "subscriptionEndsAt": 1569691245
        }
        self._logger.info(json.dumps(usage_data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(usage_data, expected_usage_data)

    def test_process_usage_with_invalid_product_plan(self):
        service = LocalPayCoDataService('tests/resources/usage_data/invalid_product_plan')
        usage_data = service.process_usage(1)
        expected_usage_data = {}
        self._logger.info(json.dumps(usage_data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(usage_data, expected_usage_data)
