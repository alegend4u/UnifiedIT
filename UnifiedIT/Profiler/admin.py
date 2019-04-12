from django.contrib import admin
from .models import *

institute_name = 'insname' # TODO: Make this dynamic

institute_site = admin.AdminSite(institute_name)


class PersonAdmin(admin.ModelAdmin):
    using = institute_name

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super(PersonAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        return super(PersonAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        return super(PersonAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


class AddressAdmin(admin.ModelAdmin):
    using = institute_name

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super(AddressAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        return super(AddressAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        return super(AddressAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


class ContactAdmin(admin.ModelAdmin):
    using = institute_name

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super(ContactAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        return super(ContactAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        return super(ContactAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


admin.site.register(Person, PersonAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Contact, ContactAdmin)
