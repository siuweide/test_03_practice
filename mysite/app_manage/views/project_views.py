from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render, redirect

from app_manage.models import Project,Module
from app_manage.forms import ProjectForms,ProjectEditForms

def manage(request):
    return render(request, 'manage.html')

def project_list(request):
    """  项目管理列表 """
    projectList = Project.objects.all().order_by('-create_time')
    p = Paginator(projectList, 5)
    page = request.GET.get('page', '')
    if page == '':
        page = 1
    try:
        projectList = p.page(page)
    except PageNotAnInteger:
        projectList = p.page(1)
    except EmptyPage:
        projectList = p.page(p.num_pages)
    return render(request, 'projects/list.html', {
        'projectList':projectList
    })

def project_add(request):
    """ 添加项目 """
    if request.method == "GET":
        forms = ProjectForms()
        return render(request, 'projects/add.html', {
            'forms': forms
        })
    elif request.method == "POST":
        forms = ProjectForms(request.POST)
        if forms.is_valid():
            # 通过forms.cleaned_data获取表单name的数据
            name = forms.cleaned_data['name']
            describe = forms.cleaned_data['describe']
            status = forms.cleaned_data['status']
            if name == '' or describe == '':
                errors = '项目名称或者描述不能为空'
                return render(request, 'projects/add.html', {
                    'forms': forms,
                    'errors':errors
                })
            # 获取表单的数据后，然后创建
            Project.objects.create(name=name, describe=describe, status=status)
            return redirect('/manage/project_list/')

def project_edit(request,pid):
    """ 编辑项目 """
    if request.method == "GET":
        if pid:
            project = Project.objects.get(id=pid)
            forms = ProjectEditForms(instance=project)
        else:
            forms = ProjectForms()
        return render(request, 'projects/edit.html', {
            'forms':forms,
            'pid': pid
        })
    elif request.method == "POST":
        forms = ProjectEditForms(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            describe = forms.cleaned_data['describe']
            status = forms.cleaned_data['status']

            p = Project.objects.get(id=pid)
            p.name = name
            p.describe = describe
            p.status = status
            p.save()
        return redirect('/manage/project_list/')

def project_delete(request,pid):
    """ 删除项目 """
    if request.method == "GET":
        p = Project.objects.get(id=pid)
        p.delete()
        return redirect("/manage/project_list/")


