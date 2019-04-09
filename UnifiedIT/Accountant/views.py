from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from Accountant import forms
from Accountant import models


# Create your views here.


def index(request):

    if request.session.get('username'):
        page = 'dashboard.html'
        logged_in = True
        username = request.session.get('username')
    else:
        page = 'index.html'
        logged_in = False
        username = ''

    return render(request, page, {
        'logged_in': logged_in,
        'username': username
    })


# Institute Admin Login View
def admin_login(request):

    validation_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            account_request = models.AccountRequest.objects.get(username=username)

            if account_request.account_link.user_password == password:
                request.session['username'] = username
                request.session['institute_name'] = account_request.institute_name
                return HttpResponseRedirect(reverse(index))

        except models.AccountRequest.DoesNotExist as dne:
            print('Username and Password didn\'t match:\n', dne)
            validation_message = "Provided Username and Password didn't match our records."

    return render(request, 'Accountant/admin_login.html', context={
        'validation_message': validation_message
    })


def admin_logout(request):

    if request.session.get('username'):
        del request.session['username']
    return HttpResponseRedirect(reverse('index'))


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

    return render(request, 'Accountant/get_account.html', {'user_form': user_form, 'registered': registered})
