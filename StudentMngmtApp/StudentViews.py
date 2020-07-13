from django.http import HttpResponseRedirect
from django.shortcuts import render


def student_home(request):
    return render(request,"student_template/student_home_template.html")