from django import forms

class CourseEmailForm(forms.Form):
    course_name = forms.CharField(max_length=50)
    email = forms.EmailField()