from django.urls import path
from app_manage.views import project_views
from app_manage.views import module_views

urlpatterns = [
    # 管理页面
    path('', project_views.manage),
    # 项目管理列表
    path('project_list/', project_views.project_list),
    # 添加项目
    path('project_add/', project_views.project_add),
    # 编辑项目
    path('project_edit/<int:pid>/', project_views.project_edit),
    # 删除项目
    path('project_delete/<int:pid>/', project_views.project_delete),

    # 模块管理列表
    path('module_list/', module_views.module_list),
    # 添加模块
    path('module_add/', module_views.module_add),
    # 编辑模块
    path('module_edit/<int:mid>/', module_views.module_edit),
    # 删除模块
    path('module_delete/<int:mid>/', module_views.module_delete)

]