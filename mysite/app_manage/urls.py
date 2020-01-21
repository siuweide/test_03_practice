from django.urls import path
from app_manage import views


urlpatterns = [
    # 管理页面
    path('', views.manage),
    # 项目管理
    path('project_list', views.project_list)
]