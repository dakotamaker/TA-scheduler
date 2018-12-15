from django import forms

class CourseEmailForm(forms.Form):
    course_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))