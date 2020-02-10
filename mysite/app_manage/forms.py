from django import forms
from django.forms import widgets
from app_manage.models import Project,Module

class ProjectForms(forms.Form):
    """ 添加项目 """
    name = forms.CharField(label='项目名称',
                           max_length=100,
                           widget=widgets.TextInput(attrs={'class':'form-control'}))
    describe = forms.CharField(label='描述',
                               max_length=200,
                               widget=widgets.Textarea(attrs={'class':'form-control'}))
    status = forms.BooleanField(label='状态',required=False,
                                widget=widgets.CheckboxInput())

class ProjectEditForms(forms.ModelForm):
    """ 编辑项目 """

    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']

class ModuleForms(forms.ModelForm):
    """ 添加模块"""

    class Meta:
        model = Module
        fields = ['project', 'name', 'describe']
        widgets = {
            'name':forms.widgets.TextInput(attrs={'class':'form-control'}),
            'describe':forms.widgets.Textarea(attrs={'class':'form-control'}),
        }