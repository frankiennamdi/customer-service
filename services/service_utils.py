import re

from services.constants import Constants
from services.metadata_validator import MetadataValidator, Result


class ServiceUtils:

    @classmethod
    def is_valid_licensed_product(cls, product_dict):
        if Constants.METADATA_KEY not in product_dict:
            return False
        metadata_dict = product_dict[Constants.METADATA_KEY]
        if MetadataValidator.validate_request_size(metadata_dict).result == Result.VALID \
                and MetadataValidator.validate_storage(metadata_dict).result == Result.VALID \
                and MetadataValidator.validate_api_calls(metadata_dict).result == Result.VALID:
            return True
        else:
            return False

    @classmethod
    def is_keys_exists(cls, dictionary, *keys):
        """
        Check if *keys exist in the diction.
        """
        if not isinstance(dictionary, dict):
            raise ValueError('expects dict as first argument.')
        if len(keys) == 0:
            raise ValueError('expects at least two arguments, one given.')

        _curr_dictionary = dictionary
        for key in keys:
            try:
                _curr_dictionary = _curr_dictionary[key]
            except KeyError:
                return False
        return True

    @classmethod
    def get_id(cls, prefix, id_str):
        match = re.search(r"{}_(?P<id>\d+)".format(prefix), id_str)
        return match.group('id')
