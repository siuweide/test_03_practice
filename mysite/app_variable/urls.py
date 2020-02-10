from django.urls import path
from app_variable import views

urlpatterns = [
    # 变量管理列表
    path('variable_list/', views.variable_list),
    # 保存自定义变量
    path('variable_save/', views.variable_save),
    # 删除自定义变量
    path('variable_delete/', views.variable_delete)
    ]