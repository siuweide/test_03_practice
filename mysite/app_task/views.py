import json
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from app_manage.models import Project,Module
from app_case.models import TestCase
from app_task.models import TestTask, TestResult
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app_task.extend.task_thread import TestThread

def task_list(request):
    taskList = TestTask.objects.all()
    p = Paginator(taskList, 5)
    page = request.GET.get('page')
    if page == '':
        page =1
    try:
        taskList = p.page(page)
    except PageNotAnInteger:
        taskList = p.page(1)
    except EmptyPage:
        taskList = p.page(p.num_pages)
    return render(request, 'task/list.html', {
        'taskList':taskList
    })

def task_add(request):
    return render(request, 'task/add.html', {
        'task_add':task_add
    })

def task_edit(request, tid):
    # 编辑用例
    return render(request, 'task/edit.html')

def case_node(request):
    if request.method == "GET":
        data = []
        project_list = Project.objects.all()

        for p in project_list:
            project_dict = {
                "name":p.name,
                "isParent":True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name":m.name,
                    "isParent":True
                }
                module_list.append(module_dict)
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    case_dict = {
                        "id":c.id,
                        "name":c.name,
                        "isParent":False
                    }
                    case_list.append(case_dict)
                module_dict['children'] = case_list
            project_dict['children'] = module_list
            data.append(project_dict)
        return JsonResponse({"code":10200, "message":"success", "data":data})

    elif request.method == "POST":
        tid = request.POST.get("tid", "")
        task = TestTask.objects.get(id=tid)
        case_list = task.cases[1:-1].split(",")
        case_list_int = []
        for c in case_list:
            try:
                case_list_int.append(int(c))
            except ValueError:
                print('任务用例为空')
        task_data = {
            "taskName": task.name,
            "taskDesc": task.describe
        }

        data = []
        project_list = Project.objects.all()

        for p in project_list:
            project_dict = {
                "name":p.name,
                "isParent":True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name":m.name,
                    "isParent":True
                }
                module_list.append(module_dict)
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    if c.id in case_list_int:
                        case_dict = {
                            "id":c.id,
                            "name":c.name,
                            "isParent":False,
                            "checked": True
                        }
                    else:
                         case_dict = {
                            "id":c.id,
                            "name":c.name,
                            "isParent":False,
                            "checked": False
                        }
                    case_list.append(case_dict)
                module_dict['children'] = case_list
            project_dict['children'] = module_list
            data.append(project_dict)

        task_data['data'] = data
        return JsonResponse({"code":10200, "message":"success", "data":task_data})

def task_save(request):
    # 保存用例
    if request.method == "POST":
        tid = request.POST.get("tid")
        task_name = request.POST.get("name")
        task_desc = request.POST.get("desc")
        task_cases = request.POST.get("cases")
        print('task_name-------->',task_name)
        print('task_desc-------->',task_desc)
        print('task_cases-------->',task_cases)

        if task_name == '':
            return JsonResponse({"code":10101, "message":"用例名称不能为空!"})
        if task_cases == '':
            return JsonResponse({"code":10102, "message":"用例不能为空!"})

        if tid == "0":
            print("进入到0------------>")
            TestTask.objects.create(name=task_name,
                                    describe=task_desc,
                                    cases=task_cases)
        else:
            testtask = TestTask.objects.get(id=tid)
            testtask.name = task_name
            testtask.describe = task_desc
            testtask.cases = task_cases
            testtask.save()
        return JsonResponse({"code":10200, "message":"创建任务成功"})
    else:
        return JsonResponse({"code":10104, "message":"请求方法错误"})

def task_delete(request):
    # 删除任务
    if request.method == "POST":
        tid = request.POST.get("taskID", "")
        task = TestTask.objects.get(id=tid)
        task.delete()
        return JsonResponse({"code":10200, "message":"删除用例成功!"})
    else:
        return JsonResponse({"code":10101, "message":"请求方法有误!"})

def task_run(request, tid):
    task = TestThread(tid)
    task.run()
    return redirect("/task/task_list/")

def task_log(request, tid):
    # 任务日志
    results = TestResult.objects.filter(task_id=tid)
    return render(request, 'task/report.html', {
        "results":results
    })

def details_log(request):
    # 任务日志详情
    rid = request.POST.get("rid", "")
    if request.method == "POST":
        r = TestResult.objects.get(id=rid)
        details = r.result
        return JsonResponse({"code":10200, "data":details})
    else:
        return JsonResponse({"code":10101, "message":"请求方法错误"})