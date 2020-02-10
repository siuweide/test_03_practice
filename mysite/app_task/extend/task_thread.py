import os
import json
import threading
from xml.dom.minidom import parse
from app_task.setting import TASK_DATA,TASK_RESULT,TASK_RUN
from app_task.models import TestTask,TestResult
from app_case.models import TestCase



class TestThread():

    def __init__(self,task_id):
        self.task_id = task_id


    def run_cases(self):
        # 1.通过任务ID获取用例数

        task = TestTask.objects.get(id=self.task_id)
        case_list = task.cases[1:-1].split(",")
        # 执行任务后将任务的状态改为执行中
        task.status = 1
        task.save()

        case_dict = {}
        for case in case_list:
            test_case = TestCase.objects.get(id=case)
            print(test_case.name)
            case_dict[test_case.name] = {
                "url":test_case.url,
                "method":test_case.method,
                "header":test_case.header,
                "par_body":test_case.parameter_body,
                "par_type":test_case.parameter_type,
                "assert_type":test_case.assert_type,
                "assert_text":test_case.assert_text
            }
        case_str = json.dumps(case_dict)

        # 2.将用例结果的数据写入到json文件里面

        with open(TASK_DATA, 'w', encoding="utf-8") as file:
            file.write(case_str)

        # 3.运行执行用例的文件
        os.system("python " + TASK_RUN)

        # 4.将结果保存到结果表里
        self.save_results()

        # 5.当任务完成后，修改任务的状态为已完成
        task = TestTask.objects.get(id=self.task_id)
        task.status = 2
        task.save()

    def save_results(self):
        f = open(TASK_RESULT, encoding="utf-8")
        xml_result = f.read()
        f.close()
        print(xml_result)
        dom = parse(TASK_RESULT)
        root = dom.documentElement
        test_suite = root.getElementsByTagName('testsuite')
        errors = test_suite[0].getAttribute("errors")
        failures = test_suite[0].getAttribute("failures")
        skipped = test_suite[0].getAttribute("skipped")
        name = test_suite[0].getAttribute("name")
        tests = test_suite[0].getAttribute("tests")
        time = test_suite[0].getAttribute("time")
        print('errors------------->',errors)
        print('failures------------->',failures)
        print('name------------->',name)

        TestResult.objects.create(task_id=self.task_id,
                                  name=name,
                                  errors=errors,
                                  failures=failures,
                                  skipped=skipped,
                                  tests=tests,
                                  run_time=time,
                                  result=xml_result)
    def run_task(self):
        t1 = threading.Thread(target=self.run_cases())
        t1.start()
        t1.join()

    def run(self):
        t = threading.Thread(target=self.run_task())
        t.start()
