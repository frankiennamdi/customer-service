import pytest

from services.local_pay_co_data_service import LocalPayCoDataService
from services.service_utils import ServiceUtils


class TestServiceUtils:

    @pytest.mark.parametrize("data_loc,product_id, valid",
                             [('resources/data', 1, True),
                              ('resources/data', 2, False),
                              ('tests/resources/data_validation/missing_data', 1, False),
                              ('tests/resources/data_validation/malformed_data', 1, False)])
    def test_licensed_product_validation(self, data_loc, product_id, valid):
        repo = LocalPayCoDataService(data_loc)
        product = repo.find_product(product_id)
        assert ServiceUtils.is_valid_licensed_product(product) is valid

    def test_get_id(self):
        assert ServiceUtils.get_id('product', 'product_2') == '2'
