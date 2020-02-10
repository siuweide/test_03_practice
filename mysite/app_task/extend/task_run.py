import os
import unittest
import requests
import xmlrunner
import json
from ddt import ddt, data, file_data, unpack

EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")

@ddt
class TestRun(unittest.TestCase):


    @file_data(TASK_DATA)
    def test_file_data_json_dict_dict(self, url, method, header, par_body, par_type, assert_type, assert_text ):

        header = json.loads(header)
        par_body = json.loads(par_body)

        if method == 1:
            res = requests.get(url, params=par_body, headers=header)
            if assert_type == 1:
                self.assertIn(assert_text, res.text)
            elif assert_type == 2:
                self.assertEqual(assert_text, res.text)
        elif method == 2:
            if par_type == 1:
                res = requests.post(url, data=par_body, headers=header)
                if assert_type == 1:
                    self.assertIn(assert_text, res.text)
                elif assert_type == 2:
                    self.assertEqual(assert_text, res.text)
            elif par_type == 2:
                res = requests.post(url, json=par_body, headers=header)
                if assert_type == 1:
                    self.assertIn(assert_text, res.text)
                elif assert_type == 2:
                    self.assertEqual(assert_text, res.text)
if __name__ == '__main__':
    with open(TASK_RESULTS, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)

