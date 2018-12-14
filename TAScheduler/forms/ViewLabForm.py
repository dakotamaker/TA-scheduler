from django import forms

#Edit user information
class ViewLabForm(forms.Form):
    course = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lab = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

