from django import forms

class LabForm(forms.Form):
    course_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    lab_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))