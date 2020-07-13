from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf.urls.static import static

# Create your views here.
from django.urls import reverse

from StudentMngmtApp.EmailBackEnd import EmailBackEnd


def ShowDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            login(request, user)
            # return HttpResponse("Email: " + request.POST.get("email") + "Password: " + request.POST.get("password"))
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect("student_home")

        else:
            messages.error(request, "Invalid Username or Password")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:

        return HttpResponse(" user: " + request.user.email + " User Type: " + str(request.user.user_type))
    else:

        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
