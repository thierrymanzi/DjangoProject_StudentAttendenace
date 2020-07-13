from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        middlename = view_func.__module__
        user = request.user
        if user.is_authenticated:

            if user.user_type == "1":

                if middlename == "StudentMngmtApp.HodViews" :
                    pass

                elif middlename == "StudentMngmtApp.views" or middlename == "django.views.static":
                    pass

                else:
                    return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2":
                if middlename == "StudentMngmtApp.StaffViews":
                    pass

                elif middlename == "StudentMngmtApp.views" or middlename == "django.views.static":
                    pass

                else:
                    return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "3":

                if middlename == "StudentMngmtApp.StudentViews":
                    pass

                elif middlename == "StudentMngmtApp.views":
                    pass

                else:
                    return HttpResponseRedirect(reverse("admin_home"))

            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:

            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass

            else:
                return HttpResponseRedirect(reverse("show_login"))
