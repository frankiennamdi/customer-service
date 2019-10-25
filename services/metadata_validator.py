import logging
import re
from enum import Enum

from services import service_utils
from services.constants import Constants

_logger = logging.getLogger(__name__)


def log_invalid_metadata(metadata_key):
    """ logging decorator for invalid metadata"""

    def wrap(function):
        def wrapper(*args, **kwargs):
            validation_result = function(*args, **kwargs)
            if validation_result.result != Result.VALID:
                _logger.warning("metadata key {} was invalid {}".format(metadata_key, validation_result))
            return validation_result

        return wrapper

    return wrap


class Result(Enum):
    """ Validation result states"""
    ABSENT = 1
    VALID = 2
    INVALID = 3


class MetadataValidationResult:
    """ Metadata validation result"""

    def __init__(self, result, value=None):
        self._result = result
        self._value = value

    @property
    def result(self):
        return self._result

    @property
    def value(self):
        return self._value

    def __str__(self):
        return "Result: {}, Value: {}".format(self.result, self.value)


class MetadataValidator:
    """ Validators for metadata"""
    SIZE_REGEX = re.compile(r"^\d+(KB|MB|GB|TB)$")
    API_CALLS_REGEX = re.compile(r"^\d+$")

    @classmethod
    @log_invalid_metadata(metadata_key=Constants.API_CALLS_KEY)
    def validate_api_calls(cls, metadata_dict):
        if service_utils.ServiceUtils.is_keys_exists(metadata_dict, Constants.API_CALLS_KEY):
            if cls.API_CALLS_REGEX.match(metadata_dict[Constants.API_CALLS_KEY]):
                return MetadataValidationResult(Result.VALID, metadata_dict[Constants.API_CALLS_KEY])
            else:
                return MetadataValidationResult(Result.INVALID, metadata_dict[Constants.API_CALLS_KEY])
        else:
            return MetadataValidationResult(Result.ABSENT)

    @classmethod
    @log_invalid_metadata(metadata_key=Constants.STORAGE_KEY)
    def validate_storage(cls, metadata_dict):
        return cls._validate_size(metadata_dict, Constants.STORAGE_KEY)

    @classmethod
    @log_invalid_metadata(metadata_key=Constants.REQUEST_SIZE_KEY)
    def validate_request_size(cls, metadata_dict):
        return cls._validate_size(metadata_dict, Constants.REQUEST_SIZE_KEY)

    @classmethod
    def _validate_size(cls, metadata_dict, size_key):
        if service_utils.ServiceUtils.is_keys_exists(metadata_dict, size_key):
            if cls.SIZE_REGEX.match(metadata_dict[size_key]):
                return MetadataValidationResult(Result.VALID, metadata_dict[size_key])
            else:
                return MetadataValidationResult(Result.INVALID, metadata_dict[size_key])
        else:
            return MetadataValidationResult(Result.ABSENT)
