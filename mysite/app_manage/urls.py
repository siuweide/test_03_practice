from django.urls import path
from app_manage import views


urlpatterns = [
    # 管理页面
    path('', views.manage),
    # 项目管理列表
    path('project_list/', views.project_list),
    # 添加项目
    path('project_add/', views.project_add),
    # 编辑项目
    path('project_edit/<int:pid>/', views.project_edit),
    # 删除项目
    path('project_delete/<int:pid>/', views.project_delete)
]