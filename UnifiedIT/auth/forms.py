from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Select a Username'
    }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your email'
    }))
    institute_name = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Institute Name'
    }))
    institute_iso = forms.CharField(max_length=255, label='', widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Institute ISO'
    }))