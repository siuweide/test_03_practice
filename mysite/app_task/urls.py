from django.urls import path
from app_task import views


urlpatterns = [
    # 任务列表
    path('task_list/', views.task_list),
    # 添加任务
    path('task_add/', views.task_add),
    # 编辑任务
    path('task_edit/<int:tid>/', views.task_edit),
    # 用例节点（树形展示）
    path('case_node/', views.case_node),
    # 保存任务
    path('task_save/', views.task_save),
    # 删除任务
    path('task_delete/', views.task_delete),
    # 运行任务
    path('task_run/<int:tid>/', views.task_run),
    # 任务日志
    path('task_log/<int:tid>/', views.task_log),
    # 详情日志
    path('details_log/', views.details_log),
]

