from django.contrib import admin
from django.contrib.auth.models import User, Group
from Accountant.models import AccountRequest, Account

from Accountant.db_creator import DBManager

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
            acc.user_account = acc_req
            acc.user_password = 'test_pass'  # TODO: Generate random

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

            # Assign an admin site to the institute


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
    list_display = ['username', 'institute_name', 'request_date', 'approval_date', 'approved', 'status']
    actions = [approve_request, 'delete_selected']


class AccountAdmin(admin.ModelAdmin):

    def account_user(self, account):
        return account.user_account.username

    def account_institute(self, account):
        return account.user_account.institute_name

    list_display = ['account_user', 'account_institute', 'db_name']
    actions = [delete_account, ]


main_admin.register(User)
main_admin.register(Group)
main_admin.register(AccountRequest, AccountRequestAdmin)
main_admin.register(Account, AccountAdmin)
