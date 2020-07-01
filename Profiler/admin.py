from django.contrib import admin
from .models import *


class InstituteAdmitSite(admin.AdminSite):
    site_header = "Institute Admin"


institute_admin_site = InstituteAdmitSite(name='institute_admin')


institute_admin_site.register(Person)
institute_admin_site.register(Address)
institute_admin_site.register(Contact)
