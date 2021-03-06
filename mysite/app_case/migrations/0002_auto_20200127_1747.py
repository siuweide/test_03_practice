# Generated by Django 2.1 on 2020-01-27 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_case', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='assert_type',
            field=models.SmallIntegerField(choices=[('1', 'include'), ('2', 'equal')], default='1', verbose_name='断言类型'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='method',
            field=models.SmallIntegerField(choices=[('1', 'GET'), ('2', 'POST')], default='1', verbose_name='请求方法'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='parameter_type',
            field=models.SmallIntegerField(choices=[('1', 'form-data'), ('2', 'json')], default='1', verbose_name='参数类型'),
        ),
    ]
