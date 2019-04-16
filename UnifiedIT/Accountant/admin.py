from django.contrib import admin
from django.contrib.auth import get_user_model
from Accountant.models import AccountRequest, Account
from Accountant.db_creator import DBManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Accountant.forms import UserChangeForm, UserCreationForm

from django.utils import timezone
# Register your models here.


class MainAdmin(admin.AdminSite):
    site_header = 'UnifiedIT Administration'


main_admin = MainAdmin(name='mainadmin')
main_admin.disable_action('delete_selected')


def approve_request(model_admin, request, query_set):
    for acc_req in query_set:
        if not acc_req.approved:

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
            acc.user.account_link = acc
            acc.db_key = account_db_name  # Using a separate field to store database key for settings.DATABASE

            acc.db_engine = db_details['ENGINE']
            acc.db_name = db_details['NAME']
            acc.db_user = db_details['USER']
            acc.db_password = db_details['PASSWORD']
            acc.db_host = db_details['HOST']
            acc.db_port = db_details['PORT']

            acc.save()

            # Save the Account Request
            acc_req.approved = True
            acc_req.approval_date = timezone.now()
            acc_req.account_link = acc

            acc_req.save()

            # TODO: Email the credentials to the user.


approve_request.short_description = 'Grant selected requests'


def delete_account(model_admin, request, query_set):
    for account in query_set:
        acc_req = AccountRequest.objects.get(username=account.user_account.username)
        acc_req.status = 'Dead'
        acc_req.save()
        acc = DBManager(str(account))
        acc.delete()
        account.delete()


delete_account.short_description = 'Delete selected accounts'


class AccountRequestAdmin(admin.ModelAdmin):
    list_display = ['username', 'institute_name', 'request_date', 'approval_date', 'approved']
    actions = [approve_request, 'delete_selected']


class AccountAdmin(admin.ModelAdmin):

    def account_user(self, account):
        return account.user.username

    def account_institute(self, account):
        return account.details.institute_name

    list_display = ['account_user', 'account_institute', 'db_key', 'status']
    actions = [delete_account, ]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_institute_admin')
    list_filter = ('is_institute_admin',)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


main_admin.register(get_user_model(), UserAdmin)
# main_admin.register(Group)
main_admin.register(AccountRequest, AccountRequestAdmin)
main_admin.register(Account, AccountAdmin)
