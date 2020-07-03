import re

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

from Accountant.db_manager import DBManager
from Accountant.forms import CustomUserCreationForm, CustomUserChangeForm
from Accountant.models import *


class MainAdmin(admin.AdminSite):
    site_header = 'UnifiedIT Administration'


main_admin = MainAdmin(name='main_admin')
main_admin.disable_action('delete_selected')


def approve_request(model_admin, request, query_set):
    for acc_req in query_set:
        if acc_req.status != 'approved':
            # Create a separate DB for the same
            # Using 'institute_name' as DB_NAME
            account_db_name = re.sub(r'\s+', '_', acc_req.institute_name)
            db_man = DBManager(account_db_name)
            db_details = db_man.create()
            if not db_details:
                return

            # Create an account for this user
            acc = Account()
            acc.details = acc_req
            acc.user = get_user_model().objects.create_user(
                username=acc_req.username,
                email=acc_req.email,
                password='ins_admin',  # TODO: Generate Random
                is_institute_admin=True,
                is_staff=True
            )
            acc.db_key = account_db_name  # Store database key for settings.DATABASE (usage: settings.DATABASE[acc.db_key])

            acc.db_details = db_details

            acc.user.account_link = acc  # This doesn't work actually

            acc.save()

            acc_user = User.objects.get(pk=acc.user.id)  # So taking a separate user var
            acc_user.account_link = acc
            acc_user.save()

            # Save the Account Request
            acc_req.status = 'approved'
            acc_req.approval_date = timezone.now()
            acc_req.account_link = acc

            acc_req.save()

            # TODO: Email the credentials to the user.


approve_request.short_description = 'Grant selected requests'


def delete_account(model_admin, request, query_set):
    for account in query_set:
        acc_req = AccountRequest.objects.filter(username=account.user.username).first()
        if acc_req is not None:
            acc_req.status = 'dead'
            acc_req.save()
        accdb = DBManager(account.db_key)
        acc_user = User.objects.get(username=account.user.username)
        acc_user.delete()
        account.delete()
        accdb.delete()


delete_account.short_description = 'Delete selected accounts'


class AccountRequestAdmin(admin.ModelAdmin):
    list_display = ['username', 'institute_name', 'request_date', 'approval_date', 'status']
    actions = [approve_request, 'delete_selected']


class AccountAdmin(admin.ModelAdmin):

    def account_user(self, account):
        return account.user.username

    def account_institute(self, account):
        if account.details is not None:
            return account.details.institute_name
        else:
            return 'None'

    list_display = ['account_user', 'account_institute', 'db_key', 'status']
    actions = [delete_account, ]


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'is_institute_admin', 'is_superuser')
    list_filter = ('is_institute_admin',)

    actions = ['delete_selected', ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_institute_admin',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Account', {'fields': ('account_link',)})
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Institute Info', {
            'fields': ('is_institute_admin', 'account_link',)
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if not form.cleaned_data['is_institute_admin'] or not form.cleaned_data['is_institute_admin']:
            obj.account_link = None
            obj.is_institute_admin = False

        super().save_model(request, obj, form, change)


main_admin.register(get_user_model(), CustomUserAdmin)
main_admin.register(AccountRequest, AccountRequestAdmin)
main_admin.register(Account, AccountAdmin)
