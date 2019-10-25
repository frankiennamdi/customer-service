import json
import logging
from urllib.parse import urlencode

from tests.test_utils import TestUtils


def response_json(response):
    return json.loads(response.data.decode())


def to_json(**kwargs):
    return json.dumps(kwargs)


def url_string(**url_params):
    string = '/api/customer'
    if url_params:
        string += '?' + urlencode(url_params)

    return string


def prepare_query(query_str):
    return query_str.replace('\r', ' ').replace('\n', ' ')


def assert_equals(list_of_dict_one, list_of_dict_two):
    pairs = zip(list_of_dict_one, list_of_dict_two)
    assert any(x != y for x, y in pairs)


def query(service, id):
    query_str = """
            query {
              %s(customerId: %s){
                    subscriptionStartsAt
                    subscriptionEndsAt
                    status
                    allowsApiOverage
                    details
                    {
                        apiCalls
                        storage
                        requestSize
                    }
                }
            }
            """ % (service, id)
    prepared_query = prepare_query(query_str)
    return to_json(query=prepared_query)


class TestCustomerGraphQlView:
    _logger = logging.getLogger(__name__)

    def test_find_customer_usage_with_valid_product_plan_and_subscription(self, flask_test_client):
        response = flask_test_client.post(url_string(), data=query('customer', 1), content_type='application/json')

        assert response.status_code == 200
        data = response_json(response)
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
        self._logger.info(json.dumps(data, indent=4, sort_keys=True))
        assert TestUtils.assert_equals(data['data']['customer'], expected_usage_data)

    def test_find_customer_usage__with_invalid_product_plan(self, flask_test_client):
        response = flask_test_client.post(url_string(), data=query('customer', 4), content_type='application/json')
        assert response.status_code == 200
        data = response_json(response)
        self._logger.info(json.dumps(data, indent=4, sort_keys=True))
        assert data['data']['customer'] is None
