from django.urls import path
from app_case import views


urlpatterns = [
    # 用例列表
    path('case_list/', views.case_list),
    # 创建用例
    path('case_add/', views.case_add),
    # 发送请求
    path('send_req/', views.send_req),
    # 断言结果
    path('assert_result/', views.assert_result),
    # 获取项目/模块（供下拉框使用）
    path('get_select_data/', views.get_select_data),
    # 保存用例
    path('save_case/', views.save_case),
    # 用例的编辑
    path('case_edit/<int:cid>/', views.case_edit),
    # 获取用例信息
    path('get_case_info/', views.get_case_info),
    # 删除用例
    path('case_delete/', views.case_delete)
]