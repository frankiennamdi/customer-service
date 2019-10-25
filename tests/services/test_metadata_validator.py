import pytest

from services.metadata_validator import MetadataValidationResult, Result, MetadataValidator


class TestMetadataValidator:

    @pytest.mark.parametrize("input_dict,expected_validation_result",
                             [({'apiCalls': '2000'}, MetadataValidationResult(Result.VALID, '2000')),
                              ({'apiCalls': '-1000'}, MetadataValidationResult(Result.INVALID, "-1000")),
                              ({}, MetadataValidationResult(Result.ABSENT))
                              ])
    def test_api_calls_validation(self, input_dict, expected_validation_result):
        validation_result = MetadataValidator.validate_api_calls(input_dict)
        assert validation_result.value == expected_validation_result.value
        assert validation_result.result == expected_validation_result.result

    @pytest.mark.parametrize("input_dict,expected_validation_result",
                             [({'requestSize': '2TB'}, MetadataValidationResult(Result.VALID, '2TB')),
                              ({'requestSize': '100 MB'}, MetadataValidationResult(Result.INVALID, '100 MB')),
                              ({}, MetadataValidationResult(Result.ABSENT))
                              ])
    def test_request_size(self, input_dict, expected_validation_result):
        validation_result = MetadataValidator.validate_request_size(input_dict)
        assert validation_result.value == expected_validation_result.value
        assert validation_result.result == expected_validation_result.result

    @pytest.mark.parametrize("input_dict,expected_validation_result",
                             [({'storage': '2TB'}, MetadataValidationResult(Result.VALID, '2TB')),
                              ({'storage': '100 MB'}, MetadataValidationResult(Result.INVALID, '100 MB')),
                              ({}, MetadataValidationResult(Result.ABSENT))
                              ])
    def test_storage_size(self, input_dict, expected_validation_result):
        validation_result = MetadataValidator.validate_storage(input_dict)
        assert validation_result.value == expected_validation_result.value
        assert validation_result.result == expected_validation_result.result
