# Generated by Django 2.1 on 2020-02-03 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('describe', models.TextField(default='', verbose_name='描述')),
                ('status', models.SmallIntegerField(choices=[('0', '未执行'), ('1', '执行中'), ('2', '已完成')], default='0', verbose_name='状态')),
                ('cases', models.TextField(default='', verbose_name='关联用例')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
    ]
