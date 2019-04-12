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

        if request.user.is_staff:
            # TODO: Determine whether admin staff accessing which institute
            # and select relevant database.
            pass
        else:
            db_name = request.session.get('institute_name')


class ProfilerRouter:

    def db_for_read(self, model, **hints):
        print('db w/r model: ', model)
        if model._meta.app_label == 'Profiler':
            if db_name:
                print('Database selected: ', db_name)
                return db_name
            print('Database selected for read: admin_db')
        return "admin_db"

    def db_for_write(self, model, **hints):
        print('db w/r model: ', model)
        if model._meta.app_label == 'Profiler':
            if db_name:
                print('Database selected: ', db_name)
                return db_name
            print('Database selected for read: admin_db')
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