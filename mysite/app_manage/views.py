from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def manage(request):
    return render(request, 'manage.html')

def project_list(request):
    pass