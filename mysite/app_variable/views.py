from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from app_variable.models import Variable

def variable_list(request):

    variable = Variable.objects.all()
    print('variable------------->',variable)
    p = Paginator(variable,5)
    page = request.GET.get('page')
    print('page-------------->', page)
    if page == '':
        page = 1
    try:
        variable = p.page(page)
        print('cases---------------->', variable)
    except PageNotAnInteger:
        # 如果页数不是证数，取第一页
        variable = p.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        variable = p.page(p.num_pages)
    return render(request, 'variable/list.html', {
        'variable':variable
    })


def variable_save(request):
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        key = request.POST.get("req_key", "")
        value = request.POST.get("req_val", "")
        desc = request.POST.get("req_desc", "")
        print("vid------->",type(vid),vid)


        if key == "" or value == "":
            return JsonResponse({"code":10101, "message":"键或值不能为空!"})

        if vid == "0":
            print("-----------进入到创建变量------------")
            Variable.objects.create(key=key, value=value, describe=desc)
        else:
            print("-----------进入到编辑变量------------")
            variable = Variable.objects.get(id=vid)
            variable.key = key
            variable.value = value
            variable.describe = desc
            variable.save()
        return JsonResponse({"code":10200, "message":"保存变量成功!"})
    else:
        return JsonResponse({"code":10102, "message": "请求方法错误!"})

def variable_delete(request):
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        variable = Variable.objects.get(id=vid)
        variable.delete()
        return JsonResponse({"code":10200, "message":"删除自定义变量成功"})
    else:
        return JsonResponse({"code":10101, "message":"请求方法错误"})
