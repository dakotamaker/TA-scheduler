from django import forms

#Edit user information
class ViewCourseForm(forms.Form):
    course = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

