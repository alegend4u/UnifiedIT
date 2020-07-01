from .models import User
from django.contrib.auth.hashers import check_password


class CustomBackend:

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            print('user value =', user, password)

            password_valid = check_password(password=password, encoded=user.password)
            if password_valid:
                if user.is_superuser or user.is_institute_admin:
                    print('returning user')
                    return user
                return None
            else:
                print('password not matched')
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    # def has_perm(self, user_obj, perm, obj=None):
    #     print('bam')
    #     return user_obj.is_superuser or user_obj.is_institute_admin
    #
    # def has_module_perm(self, app_label):
    #     if app_label == 'Accountant':
    #         return
