global db_name
db_name = ''


class RouterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, args, kwargs):
        global db_name
        db_name = request.session.get('institute_name')


class ProfilerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Profiler':
            if db_name:
                print('Database selected: ', db_name)
                return db_name
            print('Database selected for read: ', db_name)
        return "admin_db"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'Profiler':
            if db_name:
                print('Database selected: ', db_name)
                return db_name
            print('Database selected for read: admin_db')
        return "admin_db"

    def allow_relation(self, obj1, obj2, **hints):
        app_labels = [obj1._meta.app_label, obj2._meta.app_label]

        # if obj1._meta.app_label == 'Accountant' or \
        #    obj2._meta.app_label == 'Accountant':
        if 'auth' in app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        print('{}.{}, db = {}, hints = {}'.format(app_label, model_name, db, str(hints)), end=' ')
        if app_label == 'Profiler':
            print(db == 'insname')
            return db == 'insname'
        print(db == 'admin_db')
        return db == 'admin_db'
