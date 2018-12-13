from django import forms

class LabForm(forms.Form):
    course_name = forms.CharField(max_length=50)
    lab_name = forms.CharField(max_length=50)