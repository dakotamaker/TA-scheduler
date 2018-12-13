from django import forms


class UserInfoForm(forms.Form):
    email = forms.EmailField()
    fname = forms.CharField(max_length=50, label='First name')
    lname = forms.CharField(max_length=50, label='Last name')
    role_id = forms.IntegerField()
    phone = forms.CharField(max_length=50, label='Phone number')
    address = forms.CharField(max_length=255)
    office_hours = forms.CharField(max_length=50, required=False)
    office_location = forms.CharField(max_length=50, required=False)