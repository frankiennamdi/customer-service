import json


class TestUtils:

    @staticmethod
    def assert_equals(dict_one, dict_two):
        one = json.dumps(dict_one, sort_keys=True)
        two = json.dumps(dict_two, sort_keys=True)
        return one == two
