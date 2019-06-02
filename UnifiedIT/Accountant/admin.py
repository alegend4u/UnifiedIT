from django.contrib import admin
from django.contrib.auth import get_user_model
from Accountant.models import *
from Accountant.db_creator import DBManager
from django.contrib.auth.admin import UserAdmin
from Accountant.forms import CustomUserCreationForm, CustomUserChangeForm

from django.utils import timezone
# Register your models here.


class MainAdmin(admin.AdminSite):
    site_header = 'UnifiedIT Administration'


main_admin = MainAdmin(name='main_admin')
main_admin.disable_action('delete_selected')


def approve_request(model_admin, request, query_set):
    for acc_req in query_set:
        if not acc_req.status == 'approved':

            # Create a separate DB for the same
            # Using 'institute_name' as DB_NAME
            account_db_name = acc_req.institute_name.replace(' ', '_')
            db_man = DBManager(account_db_name)
            db_details = db_man.create()

            # Create an account for this user
            acc = Account()
            acc.details = acc_req
            acc.user = get_user_model().objects.create_user(
                username=acc_req.username,
                email=acc_req.email,
                password='ins_admin',  # TODO: Generate Random
                is_institute_admin=True
            )
            acc.db_key = account_db_name  # Using a separate field to store database key for settings.DATABASE

            acc.db_engine = db_details['ENGINE']
            acc.db_name = db_details['NAME']
            acc.db_user = db_details['USER']
            acc.db_password = db_details['PASSWORD']
            acc.db_host = db_details['HOST']
            acc.db_port = db_details['PORT']

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
        acc_req = AccountRequest.objects.get(username=account.user.username)
        acc_req.status = 'dead'
        acc_req.save()
        acc = DBManager(str(account))
        acc_user = User.objects.get(username=account.user.username)
        acc_user.delete()
        acc.delete()
        account.delete()


delete_account.short_description = 'Delete selected accounts'


class AccountRequestAdmin(admin.ModelAdmin):
    list_display = ['username', 'institute_name', 'request_date', 'approval_date', 'status']
    actions = [approve_request, 'delete_selected']


class AccountAdmin(admin.ModelAdmin):

    def account_user(self, account):
        return account.user.username

    def account_institute(self, account):
        return account.details.institute_name

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
