import unittest
import requests
import xmlrunner
from ddt import ddt, data, file_data, unpack

@ddt
class TestRun(unittest.TestCase):

    # def test_case(self):
    #     res = requests.get(url="http://www.baidu.com")
    #     print(res.text)

    @file_data("./test_data.json")
    def test_file_data_json_dict_dict(self, url, method, per):
        if method == "get":
            res = requests.get(url, params=per)
            print(res.text)

if __name__ == '__main__':
    with open('./test_results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)