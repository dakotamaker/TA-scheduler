from django import forms


class CourseNameForm(forms.Form):
    course_name = forms.CharField(max_length=50)

