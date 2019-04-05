from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Auth import forms
from Auth import models

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'Auth/login.html')

def get_account(request):
    registered = False
    user_form = forms.UserForm()

    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            institute_name = user_form.cleaned_data['institute_name']
            institute_iso = user_form.cleaned_data['institute_iso']
            registered = True

            # Save the request to the DB
            account_request = models.AccountRequest(username=username, email=email, 
                institute_name=institute_name, institute_iso=institute_iso)
            account_request.save()

            print(username, email, institute_name, institute_iso)
            


    return render(request, 'Auth/get_account.html', {'user_form': user_form, 'registered': registered})