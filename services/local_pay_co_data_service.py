import json
from distutils.util import strtobool
from os import path

from file_finder import FileFinder
from services import service_utils
from services.constants import Constants

from services.service_utils import ServiceUtils


class RecordNotFoundError(Exception):
    """ Thrown when a record is not found"""

    def __init__(self, *args, **kwargs):
        pass


class UsageInfo:
    """" Holds the usage information"""

    def __init__(self):
        self._usage_data = {}

    def update_usage_data(self, update_usage_data_dict):
        # if the new data has details, then it is valid, regardless of active status
        if ServiceUtils.is_keys_exists(update_usage_data_dict, 'details'):
            if not self._usage_data:
                self._usage_data = update_usage_data_dict
            elif self._usage_data['status'] != 'active' and update_usage_data_dict['status'] == 'active':
                self._usage_data = update_usage_data_dict

    @property
    def usage_data(self):
        return self._usage_data


class LocalPayCoDataService:
    # mapping for active and inactive
    SUBSCRIPTION_STATUS_MAP = {
        'active': 'active',
        'trialing': 'active',
        'past_due': 'active',
        'inactive': 'inactive',
        'unpaid': 'inactive',
    }

    METERED_USAGE_TYPE = 'metered'
    LICENSED_USAGE_TYPE = 'licensed'

    def __init__(self, data_directory):
        self._data_directory = data_directory

    def find_product(self, product_id):
        return self._find('product', product_id)

    def find_customer(self, customer_id):
        return self._find('customer', customer_id)

    def _find(self, data_type, id):
        file = FileFinder.resolve("{}/{}{}.json".format(self._data_directory, data_type, id))
        if not file or not path.exists(file):
            return None

        with open(file) as json_file:
            return json.load(json_file)

    def process_usage(self, customer_id):
        customer = self.find_customer(customer_id)
        if customer is None:
            raise RecordNotFoundError("Record With Customer Id {} Not Found".format(customer_id))

        if Constants.SUBSCRIPTIONS_KEY not in customer:
            return None

        subscriptions = customer[Constants.SUBSCRIPTIONS_KEY]
        if Constants.SUBSCRIPTIONS_DATA_KEY not in subscriptions:
            return None

        usage_info = UsageInfo()
        for subscription_data in subscriptions[Constants.SUBSCRIPTIONS_DATA_KEY]:
            if not ServiceUtils.is_keys_exists(subscription_data, 'items', 'data'):
                continue
            current_usage_data = {
                'status': self.SUBSCRIPTION_STATUS_MAP[subscription_data['status']],
                'subscriptionStartsAt': subscription_data['current_period_start'],
                'subscriptionEndsAt': subscription_data['current_period_end'],
                'allowsApiOverage': False
            }

            for subscription_item in subscription_data['items']['data']:
                if subscription_item['plan']['usage_type'] == self.METERED_USAGE_TYPE and strtobool(str(
                        subscription_item['plan']['active'])):
                    current_usage_data['allowsApiOverage'] = True

                if subscription_item['plan']['usage_type'] == self.LICENSED_USAGE_TYPE:
                    licensed_product_id = ServiceUtils.get_id('product', subscription_item['plan']['product'])
                    licensed_product = self.find_product(licensed_product_id)
                    if ServiceUtils.is_valid_licensed_product(licensed_product):
                        current_usage_data['details'] = licensed_product['metadata']

            usage_info.update_usage_data(current_usage_data)
        # apply override
        usage_info = self.apply_overrides(customer, usage_info)
        return usage_info.usage_data

    def apply_overrides(self, customer, usage_info):
        if not usage_info.usage_data:
            return usage_info
        validation = service_utils.MetadataValidator.validate_api_calls(customer['metadata'])
        if validation.result == service_utils.Result.VALID:
            usage_info.usage_data['details'][Constants.API_CALLS_KEY] = validation.value

        validation = service_utils.MetadataValidator.validate_storage(customer['metadata'])
        if validation.result == service_utils.Result.VALID:
            usage_info.usage_data['details'][Constants.STORAGE_KEY] = validation.value

        validation = service_utils.MetadataValidator.validate_request_size(customer['metadata'])
        if validation.result == service_utils.Result.VALID:
            usage_info.usage_data['details'][Constants.REQUEST_SIZE_KEY] = validation.value

        return usage_info
