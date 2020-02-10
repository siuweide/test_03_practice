from django.db import models
from app_manage.models import Module

class TestCase(models.Model):
    """ 测试用例表 """
    METHOD_CHOICES = (
        ('1', 'GET'),
        ('2', 'POST')
    )
    PAR_CHOICES = (
        ('1', 'form-data'),
        ('2', 'json')
    )
    ASSERT_CHOICES=(
        ('1', 'include'),
        ('2', 'equal')
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=50, null=False)
    url = models.TextField('url', null=False)
    method = models.SmallIntegerField('请求方法', default='1',choices=METHOD_CHOICES) #1是Get请求，2是Post请求
    header = models.TextField('请求头', null=False)
    parameter_type = models.SmallIntegerField('参数类型', default='1',choices=PAR_CHOICES)
    parameter_body = models.TextField('参数内容', null=False)
    result = models.TextField('结果', null=False)
    assert_type = models.SmallIntegerField('断言类型', default='1',choices=ASSERT_CHOICES)
    assert_text = models.TextField('结果', null=False)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name
