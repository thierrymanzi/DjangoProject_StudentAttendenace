from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))

    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # These code help to select courses in dynamically
    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            select_courses = (course.id, course.course_name)
            course_list.append(select_courses)
    except:
        course_list = []

    # create a list to select session start and end year
    session_list = []
    try:
        session = SessionYearModel.objects.all()
        for ses in session:
            select_ses = (ses.id, str(ses.session_start_year) + "    TO    " + str(ses.session_end_year))
            session_list.append(select_ses)
    except:
       session_list = []

        ########--------End OF SESSION LIST-----#########

    # tuple code to select gender
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    course = forms.ChoiceField(label="Course Name", choices=course_list,
                               widget=forms.Select(attrs={"class": "form-control"}))

    sex = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Picture", widget=forms.FileInput(attrs={"class": "form-control"}))

    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class": "form-control"}),choices=session_list)


class EditStudentForm(forms.Form):
    # global session_list
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # These code help to select courses in dynamically

    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            select_courses = (course.id, course.course_name)
            course_list.append(select_courses)
    except:
            course_list = []

        # create a list to select session start and end year
    session_list = []
    try:
        session = SessionYearModel.objects.all()
        for ses in session:
            select_ses = (ses.id, str(ses.session_start_year) + "    TO    " + str(ses.session_end_year))
            session_list.append(select_ses)
    except:
            session_list = []

    # -------end for session list

    # tuple code to select gender
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    course = forms.ChoiceField(label="Course Name", choices=course_list,
                               widget=forms.Select(attrs={"class": "form-control"}))

    sex = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Picture", widget=forms.FileInput(attrs={"class": "form-control"}),required=False)

    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class": "form-control"}),choices=session_list)


