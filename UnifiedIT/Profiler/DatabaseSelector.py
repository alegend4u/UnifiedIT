from Accountant.models import Account


global db_name
db_name = ''


class RouterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, args, kwargs):
        global db_name

        if request.user.is_superuser:
            db_name = "admin_db"
        elif request.user.is_anonymous:
            db_name = ''
        elif request.user.is_institute_admin:
            current_user = Account.objects.get(user=request.user)
            db_name = current_user.db_key


class ProfilerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Profiler':
            if db_name:
                return db_name
        return "admin_db"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'Profiler':
            if db_name:
                return db_name
        return "admin_db"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if db == 'admin_db':
            return app_label in [
                'admin',
                'auth',
                'contenttypes',
                'sessions',
                'messages',
                'staticfiles',
                'Accountant'
            ]
        return app_label == 'Profiler'
