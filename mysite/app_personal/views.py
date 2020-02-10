from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
# Create your views here.

def login(request):
    if request.method == 'GET':
        print('进入到get请求')
        return render(request, 'login.html')
    elif request.method == 'POST':
        print('进入到了Post请求')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('username-------------->', username)
        print('password-------------->', password)
        user = auth.authenticate(username=username, password=password)
        print('user---------->', user)
        if user is not None:
            auth.login(request,user)
            return redirect('/manage/')
        elif username == '' or password == '':
            errors = '用户名不能为空'
            return render(request, 'login.html', {"errors":errors})
        else:
            errors = '用户名或密码错误'
            context = {'errors':errors}
            return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/login/')