from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .form import AddStudentForm, EditStudentForm
from .models import *


def admin_home(request):
    return render(request, "hod_template/home_content.html")


def add_staff(request):
    return render(request, 'hod_template/add_staff_template.html')


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")

    else:
        # password,username,first_name,last_name,email,user_type
        email = request.POST.get("email")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=firstname, last_name=lastname, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Added")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Failed To Add New Staff")
            return HttpResponseRedirect("/add_staff")

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method !="POST":
        return HttpResponseRedirect("Method Not Allowe")

    else:

        course_name =request.POST.get("course_name")
        try:
            course =Courses(course_name=course_name)
            course.save()
            messages.success(request,"Sucessfully Added course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed to Add new Course")
            return  HttpResponseRedirect("/add_course")


# Fuction to render Student home page
def add_student(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses,
    }
    form = AddStudentForm()
    return render(request, "hod_template/add_student_template.html", {"form": form})


# Function to save Student Data in our DB
def add_student_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")

    else:

        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            firstname = form.cleaned_data["first_name"]
            lastname = form.cleaned_data["last_name"]
            password = form.cleaned_data["password"]
            username = form.cleaned_data["username"]
            address = form.cleaned_data["address"]
            course_id = form.cleaned_data["course"]
            session_year_id = form.cleaned_data["session_year_id"]
            sex = form.cleaned_data["sex"]
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(firstname)

            #try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=firstname, last_name=lastname, user_type=3)
            user.Students.address = address
            course_obj = Courses.objects.get(id=course_id)
            # the is date function to convert the format d-m-y  to Y-m-d
            # He we need to convert because we want to match our inpunt date format to database format
            # sesion_start = datetime.datetime.strptime(start_year, '%d-%m-%y').strftime('%y-%m-%d')
            # sesion_end = datetime.datetime.strptime(end_year, '%d-%m-%y').strftime('%y-%m-%d')
            session_year = SessionYearModel.objects.get(id=session_year_id)
            user.students.sesion_year_id = session_year
            user.students.gender = sex
            user.students.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "New Student Successfully Added")
            return HttpResponseRedirect("/add_student")
            # except:
            messages.error(request, "Failed To Add New Student")
        # return HttpResponseRedirect("/add_student")
        else:
            form = AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses = Courses.objects.all()
    staff_obj = CustomUser.objects.filter(user_type=2)
    context = {
        "courses": courses,
        "staffs": staff_obj

    }

    return render(request, "hod_template/add_subject_template.html", context)


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")

    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff_name")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added")
            return HttpResponseRedirect("/add_subject")

        except:
            messages.error(request, "Failed To Add New Subject")
            return HttpResponseRedirect("/add_subject")


def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }

    return render(request, "hod_template/manage_staff_template.html", context)


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, "hod_template/manage_student_template.html", context)


def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, "hod_template/manage_course_template.html", context)


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, "hod_template/manage_subject_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    context = {
        "staff": staff,
        "id": staff_id
    }

    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Request Not Allowed")

    else:

        staff_id = request.POST.get("staff_id")
        email = request.POST.get("email")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.last_name = lastname
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id)

        except:
            messages.error(request, "Failed To Edit Staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id)

#Python Function To Edit Student Form and pull all data in Database and Populate Automatically in our form
def edit_student(request, student_id):
    request.session["student_id"] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields["first_name"].initial = student.admin.first_name
    form.fields["last_name"].initial = student.admin.last_name
    form.fields["username"].initial = student.admin.username
    form.fields["email"].initial = student.admin.email
    form.fields["address"].initial = student.address
    form.fields["course"].initial = student.course_id.id
    form.fields["sex"].initial = student.gender
    form.fields["profile_pic"].initial = student.profile_pic
    form.fields["session_year_id"].initial = student.sesion_year_id

    render(request, "hod_template/edit_student_template.html",{"form": form,"id": student_id, "username": student.admin.username})


# Python Function to Edit StdentForm and Save Edited Data in our DB
def edit_student_save(request):
    if request.method != "POST":

        # return HttpResponse("Method Not Allowed")
     return HttpResponseRedirect("/manage_student")

    else:
        student_id = request.session.get("student_id")

        if student_id == None:
            return HttpResponseRedirect("/manage_student")

            form = EditStudentForm(request.POST, request.FILES)
            if form.is_valid():
                email = form.cleaned_data["email"]
                firstname = form.cleaned_data["first_name"]
                lastname = form.cleaned_data["last_name"]
                username = form.cleaned_data["username"]
                address = form.cleaned_data["address"]
                course_id = form.cleaned_data["course"]
                session_year_id = form.cleaned_data["session_year_id"]
                sex = form.cleaned_data["sex"]

                # This is sample  for uploading Picture
                # if request.FILES['profile_pic']:
                if request.FILES.get('profile_pic', False):
                    profile_pic = request.FILES['profile_pic']
                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    profile_pic_url = fs.url(filename)
                else:
                    profile_pic = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = firstname
                user.last_name = lastname
                user.email = email
                user.username = username
                user.save()
                del request.session['student_id']

                course = Courses.objects.get(id=course_id)

                student = Students.objects.get(admin=student_id)
                student.address = address
                student.course_id = course
                student.gender = sex
                if profile_pic != None:
                    student.profile_pic = profile_pic_url
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.sesion_year_id = session_year
                student.save()
                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect("/edit_student/" + student_id)
            except:
                messages.error(request, "Failed To Edit Student")
                return HttpResponseRedirect("/edit_student/" + student_id)
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, "hod_template/edit_student_template.html",{"form": form, "id": student_id, "username": student.admin.username})


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, "hod_template/edit_subject_template.html", context)


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed<h2>")

    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        staff_id = request.POST.get("staff")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            course = Courses.objects.get(id=course_id)
            staff = CustomUser.objects.get(id=staff_id)
            subject.course_id = course
            subject.staff_id = staff
            subject.save()
            messages.success(request, "Subject Edited Successfully")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
        except:
            messages.error(request, "Edit Subject Fail")
            return HttpResponseRedirect("/edit_subject/" + subject_id)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    # context={
    #     "courses":courses,
    # }
    return render(request, "hod_template/edit_course_template.html", {"course": course, "id": course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h4>Method Not Allowed</h4>")

    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
    try:
        course = Courses.objects.get(id=course_id)
        course.course_name = course_name
        course.save()
        messages.success(request, "Course Edited Successfully")
        return HttpResponseRedirect("/edit_course/" + course_id)

    except:
        messages.error(request, "Edit course Failed!!!")
        return HttpResponseRedirect("/edit_course/" + course_id)


# This is student Feedback python function
def student_feedback_message(request):
    feedbacks = FeedbackStudent.objects.all()

    return render(request, "hod_template/student_feedback_template.html", {"feddbacks": feedbacks})


@csrf_exempt  # Adding @csrf_exempt so that we can call Ajax function without using csrf_token
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedbackStaff.objects.all()

    return render(request, "hod_template/staff_feedback_template.html", {"feddbacks": feedbacks})


def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def manage_session(request):
    return render(request, "hod_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        try:
            session_start_year = request.POST.get("session_start")
            session_end_year = request.POST.get("session_end")

            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_start_year)
            sessionyear.save()
            messages.success(request,"Successfully Session Added")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
           messages.error(request,"Failed To Add Session")




