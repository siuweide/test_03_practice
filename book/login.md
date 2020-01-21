django实现登录注意点
在 index.html 页面当中:

<form action="/login_action/" method="get/post">
    <input name="username">
    <input name="password">
</form>
请求路径 login_action/
请求方法：get/post
input 标签的 name属性是传参的名称
在 views.py 文件中：

from django.contrib import auth # 使用django自带的用户模块（auth）
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        user = auth.authenticate(
            username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 验证登录
            return render(request, "project_manage.html")
        else:
            return render(request, "index.html",
                                    {"error": "用户名或者密码错误"})



@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")
request.POST.get("username", "") 获取POST请求的参数。
auth.authenticate 判断用户是否存在。
auth.login(request, user) 保留用户的登录信息。

扩展：
如果想要在页面展示登录后的用户名，可以在模板里面加入
<h3>欢迎您，{{ user.username }}</h3>

一开始引入的静态文件，如果找不到的话，要去根目录setting文件下，添加以下代码：
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)