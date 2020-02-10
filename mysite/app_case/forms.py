from django import forms
from django.forms import widgets

from app_case.models import TestCase

class TestCaseForms(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = ['module', 'name', 'url', 'method', 'header', 'parameter_type', 'parameter_body',
                  'result', 'assert_type', 'assert_text']
        widgets = {
            'name':forms.widgets.TextInput(attrs={'class':'form-control'}),
            'url':forms.widgets.TextInput(attrs={'class':'form-control'}),
            'header':forms.widgets.Textarea(attrs={'class':'form-control'}),
            'parameter_body':forms.widgets.Textarea(attrs={'class':'form-control'}),
            'result':forms.widgets.Textarea(attrs={'class':'form-control'}),
            'assert_text':forms.widgets.Textarea(attrs={'class':'form-control'}),
        }