import re
import json
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.forms import model_to_dict
from app_manage.models import Project,Module
from app_case.models import TestCase
from app_variable.models import Variable


from app_case.models import TestCase


def case_list(request):
    # 用例列表
    testCaseList = TestCase.objects.all()
    p = Paginator(testCaseList, 5)
    page = request.GET.get('page')
    if page == '':
        page = 1
    try:
        testCaseList = p.page(page)
    except PageNotAnInteger:
        testCaseList = p.page(1)
    except EmptyPage:
        testCaseList = p.page(p.num_pages)
    return render(request, 'case/list.html', {
        'testCaseList':testCaseList
    })

def case_add(request):
    # 创建用例
    if request.method == 'GET':
        return render(request, 'case/add.html')

def case_edit(request, cid):
    # 编辑用例
    if request.method == "GET":
        return render(request, 'case/edit.html')


def send_req(request):
    # 发送请求
    if request.method == 'GET':
        url = request.GET.get('url', '')
        method = request.GET.get('method', '')
        header = request.GET.get('header', '')
        cookie = request.GET.get('cookie', '')
        per_type = request.GET.get('per_type', '')
        per_value = request.GET.get('per_value', '')

        if url == "":
            return JsonResponse({"code":10101, "message":"URL不能为空!"})


        if  "${" in url and  "}" in url:
            variable_key = re.findall("\${(.+?)}", url)[0]
            print('variable----------->', variable_key)
            variable = Variable.objects.get(key=variable_key)
            url = variable.value

        if "${" in header and "}" in header:
            header = str(header)
            key = re.findall("\"\${(.+?)}\"", header)[0]
            variable = Variable.objects.get(key=key)
            real_value = variable.value
            data_list = re.findall("\"(.+?)\"", header)
            for data in data_list:
                # 将匹配出来的列表，逐一找，包含${ 和 } 的字符串取出来
                if "${" in data and "}" in data:
                    replace_value = data
            header = header.replace(replace_value, real_value)

        try:
            header = json.loads(header)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10102, "message":"Header格式错误，必须是标准的JSON格式"})

        if "${" in per_value and "}" in per_value:
            # 匹配出包含“${” 开头和 “}”结尾的值
            key = re.findall("\"\${(.+?)}\"", per_value)[0]
            # 去变量的表里查找到真正的value值
            variable = Variable.objects.get(key=key)
            real_value = variable.value
            # 在通过正则找到要替换的值（已${开头，}结尾的。）
            data_list = re.findall("\"(.+?)\"", per_value)
            for data in data_list:
                # 将匹配出来的列表，逐一找，包含${ 和 } 的字符串取出来
                if "${" in data and "}" in data:
                    replace_value = data
            per_value = per_value.replace(replace_value, real_value)

        try:
            per_value = json.loads(per_value)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10103, "message":"参数内容格式错误，必须是标准的JSON格式"})

        if cookie == 'yes':
            if method == 'get':
                r = requests.get(url, params=per_value, headers=header)
            elif method == 'post':
                if per_type == 'form':
                    r = requests.post(url, data=per_value, headers=header)
                    cookies = r.cookies
                    cookies = requests.utils.dict_from_cookiejar(cookies)
                    cookies = 'sessionid=' + cookies['sessionid']
                    variable = Variable.objects.filter(key='Cookie')
                    print('variable-------->', variable)
                    if variable:
                        variable.update(value=cookies)
                    else:
                        Variable.objects.create(key='Cookie', value=cookies)

                elif per_type == 'json':
                    r = requests.post(url, json=per_value, headers=header)
        elif cookie == 'no':
            if method == 'get':
                r = requests.get(url, params=per_value, headers=header)
            elif method == 'post':
                if per_type == 'form':
                    r = requests.post(url, data=per_value, headers=header)
                elif per_type == 'json':
                    r = requests.post(url, json=per_value, headers=header)

        return JsonResponse({"code":10200, "message":"success", "data": r.text})

def assert_result(request):
    # 断言结果
    if request.method == "GET":
        result_text = request.GET.get('result_text', '')
        assert_type = request.GET.get('assert_type', '')
        assert_result = request.GET.get('assert_result', '')

        if result_text == "" or assert_result == "":
            return JsonResponse({"code":10101, "message":"响应结果或断言结果不能为空!"})

        if assert_type == "":
            return JsonResponse({"code":10104, "message":"断言参数不能为空!"})

        if assert_type != "include" and assert_type != "equal":
            return JsonResponse({"code": 10105, "message":"断言参数错误"})

        if assert_type == "include":
            if assert_result in result_text:
                return JsonResponse({"code":10200, "message":"断言成功!"})
            else:
                return JsonResponse({"code":10102, "message":"断言失败，断言结果不包含在响应结果里面!"})
        elif assert_type == "equal":
            if assert_result == result_text:
                return JsonResponse({"code":10200, "message":"断言成功!"})
            else:
                return JsonResponse({"code":10103, "message":"断言失败，断言结果跟响应结果不相等!"})

def get_select_data(request):
    # 获取项目/模块（供下拉框使用）
    if request.method == "GET":
        projects = Project.objects.all()
        project_list = []
        for p in projects:
            project_dict = {
                "id":p.id,
                "name":p.name,
            }
            module_list = []
            modules = Module.objects.filter(project_id=p.id)
            for m in modules:
                module_dict = {
                    "id":m.id,
                    "name":m.name,
                }
                module_list.append(module_dict)
            project_dict['moduleList'] = module_list
            project_list.append(project_dict)
        return JsonResponse({"code":10200, "message":"success", "data":project_list})

def save_case(request):
    # 保存用例
    if request.method == "POST":
        case_id = request.POST.get("cid", "")
        url = request.POST.get("url", "")
        case_name = request.POST.get("case_name", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        per_type = request.POST.get("per_type", "")
        per_value = request.POST.get("per_value", "")
        print("per_value-------------->", type(per_value ), per_value)
        result_text = request.POST.get("result_text", "")
        variable = request.POST.get("variable", "")
        assert_type = request.POST.get("assert_type", "")
        assert_text = request.POST.get("assert_text", "")
        module_id = request.POST.get("module_id", "")

        if url == "":
            return JsonResponse({"code": 10101, "message": "地址不能为空!"})

        caseName = TestCase.objects.filter(name=case_name)
        if caseName.count() > 0:
            return JsonResponse({"code": 10102, "message": "用例名称不能重复!"})

        if case_name == "":
            return JsonResponse({"code": 10103, "message": "用例名称不能为空!"})


        if method == "get":
            method_int = 1
        elif method == "post":
            method_int = 2
        else:
            return JsonResponse({"code": 10104, "message": "请求方法有误!"})

        if per_type == "form":
            per_type_int = 1
        elif per_type == "json":
            per_type_int = 2
        else:
            return JsonResponse({"code":10105,"message":"参数类型错误"})

        if variable != "":
            key = variable.split('=>')[0]
            value = variable.split('=>')[1]
            real_value = re.findall(value, result_text)[0]

            variable = Variable.objects.filter(key=key)
            if variable.count() == 0:
                Variable.objects.create(key=key, value=real_value)
            else:
                return JsonResponse({"code": 10109, "message": "变量名称key不能重复!"})

        print('assert_type----------->', assert_type)
        if assert_type == "include":
            assert_type_int = 1
        elif assert_type == "equal":
            assert_type_int = 2
        else:
            return JsonResponse({"code": 10108, "message": "断言类型有误!"})

        if case_id == "":
            TestCase.objects.create(url=url, name=case_name, method=method_int, header=header, parameter_type=per_type_int,
                                    parameter_body=per_value, result=result_text, assert_type=assert_type_int,
                                    assert_text=assert_text, module_id=module_id)
            return JsonResponse({"code":10200,"message":"保存用例成功"})
        else:
            testCase = TestCase.objects.get(id=case_id)
            testCase.url = url
            testCase.name = case_name
            testCase.method = method_int
            testCase.header = header
            testCase.parameter_type = per_type_int
            testCase.parameter_body = per_value
            testCase.result = result_text
            testCase.assert_type = assert_type_int
            testCase.assert_text = assert_text
            testCase.module_id = module_id
            testCase.save()
            return JsonResponse({"code":10200,"message":"保存用例成功!"})
    else:
        return JsonResponse({"code":10109,"message":"请求方法有误!"})


def get_case_info(request):
    # 获取用例信息
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        module = Module.objects.get(id=case.module_id)
        case_infos = model_to_dict(case)
        case_infos['project'] = module.project_id
        return JsonResponse({"code":10200,"message":"查询用例成功!", "data": case_infos})
    else:
        return JsonResponse({"code":10101,"message":"请求方法错误!"})

def case_delete(request):
    # 删除用例
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        case.delete()
        return JsonResponse({"code":10200, "message":"删除成功"})
    else:
        return JsonResponse({"code":10101, "message":"请求方法错误"})