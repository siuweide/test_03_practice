from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render, redirect

from app_manage.forms import ModuleForms
from app_manage.models import Module


def module_list(request):
    """ 模块列表 """
    moduleList = Module.objects.all()
    print('moduleList------------->',moduleList)
    # 将数据做分页处理，每一页显示5条数据
    p = Paginator(moduleList,5)
    # 通过请求得到要第几页的数据
    page = request.GET.get('page')
    print('page-------------->', page)
    if page == '':
        page = 1
    try:
        moduleList = p.page(page)
        print('cases---------------->', moduleList)
    except PageNotAnInteger:
        # 如果页数不是证数，取第一页
        moduleList = p.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        moduleList = p.page(p.num_pages)
    return render(request, 'module/list.html', {
        'moduleList':moduleList
    })


def module_add(request):
    """ 添加模块 """
    if request.method == "GET":
        forms = ModuleForms()
    elif request.method == "POST":
        forms = ModuleForms(request.POST)
        if forms.is_valid():
            project = forms.cleaned_data['project']
            name = forms.cleaned_data['name']
            describe = forms.cleaned_data['describe']
            Module.objects.create(name=name, describe=describe, project=project)
            return redirect('/manage/module_list/')
    return render(request, 'module/add.html', {
        'forms':forms
    })


def module_edit(request, mid):
    """ 编辑模块 """
    if request.method == "GET":
        if mid:
            module = Module.objects.get(id=mid)
            forms = ModuleForms(instance=module)
        else:
            forms = ModuleForms()
    elif request.method == "POST":
        forms = ModuleForms(request.POST)
        if forms.is_valid():
            project = forms.cleaned_data['project']
            name = forms.cleaned_data['name']
            describe  = forms.cleaned_data['describe']

            module = Module.objects.get(id=mid)
            module.project = project
            module.name = name
            module.describe = describe

            module.save()
            return redirect('/manage/module_list')
    return render(request, 'module/edit.html', {
        "forms":forms,
        "mid":mid

    })

def module_delete(request, mid):
    """ 删除模块 """
    if request.method == "GET":
        if mid:
            module = Module.objects.get(id=mid)
            module.delete()
            return redirect('/manage/module_list/')
            # return HttpResponse('ok')