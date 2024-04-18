import unittest
from substitute import get_update_json
from pprint import pprint

class TestJsonUpdater(unittest.TestCase):

    def test_case1(self):
        data1 = {
            'a': 1,
            'b': 'hello',
            'c': True,
        }
        expected_output1 = {
            'a': {'_content': 1, '_type': "<class 'int'>"},
            'b': {'_content': 'hello', '_type': "<class 'str'>"},
            'c': {'_content': True, '_type': "<class 'bool'>"}
        }
        assert get_update_json(data1, depth=0) == expected_output1

    def test_case2(self):
        data2 = {
            'a': 1,
            'b': {
                'c': 'hello',
                'd': {
                    'e': True,
                    'f': ['foo', 'bar']
                }
            },
            'g': False
        }
        expected_output2 = {
            'a': {'_content': 1, '_type': "<class 'int'>"},
            'b': {
                'c': {'_content': 'hello', '_type': "<class 'str'>"},
                'd': {
                    'e': {'_content': True, '_type': "<class 'bool'>"},
                    'f': {'_content': ['foo', 'bar'], '_type': "<class 'list'>"}
                }
            },
            'g': {'_content': False, '_type': "<class 'bool'>"}
        }

        assert get_update_json(data2, depth=2) == expected_output2

    def test_case3(self):
        data3 = {
            'a': 1,
            'b': {
                'c': 'hello',
                'd': {
                    'e': True,
                    'f': ['foo', 'bar']
                }
            },
            'g': False
        }

        expected_output3= {
            'a': {'_content': 1, '_type': "<class 'int'>"},
            'b': {
                'c': {'_content': 'hello', '_type': "<class 'str'>"},
                'd': {
                        'e': {'_content': True, '_type': "<class 'bool'>"},
                        'f': {'_content': ['foo', 'bar'], '_type': "<class 'list'>"}
                    }
                },
                'g': {'_content': False, '_type': "<class 'bool'>"}
            }
        assert get_update_json(data3, depth=3) == expected_output3

if __name__ == "__main__":
    unittest.main()