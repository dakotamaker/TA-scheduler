from django import forms

#Edit your own information
class EditForm(forms.Form):
    phone = forms.CharField(max_length=50, label='Phone number',widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    address = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    office_hours = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    office_location = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

