from django.contrib import admin
from Auth.models import AccountRequest, Account

from Auth.db_creator import DBManager

from datetime import date
# Register your models here.


def approve_request(model_admin, request, query_set):
    for acc_req in query_set:
        if not acc_req.approved:
            acc_req.approved = True
            acc_req.approval_date = date.today()
            acc_req.save()

            # Create a separate DB for the same
            # Using 'Username' as DB_NAME
            account_db_name = acc_req.username
            db_man = DBManager(account_db_name)
            db_man.create()

            # Create an account for this user
            acc = Account()
            acc.account = acc_req
            acc.password = 'test_pass'  # Generate random

            acc.db_engine = 'test_engine'
            acc.db_name = 'test_name'
            acc.db_user = 'test_user'
            acc.db_password = 'test_db_pass'
            acc.db_host = 'test_host'
            acc.db_port = 'test_port'
            acc.save()

            # Email the credentials to the user.


approve_request.short_description = 'Grant selected requests'


class AccountRequestAdmin(admin.ModelAdmin):
    list_display = ['username', 'institute_name', 'request_date', 'approval_date']
    actions = [approve_request, ]


class AccountAdmin(admin.ModelAdmin):
    list_display = ['account', 'db_name']

    # list_display = ['account', 'ins_iso', 'db_name']
    # def ins_iso(self, acc_req):
    #     return acc_req.institute_iso


admin.site.register(AccountRequest, AccountRequestAdmin)
admin.site.register(Account, AccountAdmin)
