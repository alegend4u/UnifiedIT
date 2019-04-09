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
        institute_name = request.session.get('institute_name')
        db_name = institute_name


class ProfilerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Profiler':
            if db_name:
                print('Database selected: ', db_name)
                return db_name
            print('Database selected for read: ', db_name)
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'Profiler':
            if db_name:
                print('Database selected: ', db_name)
                return db_name
            print('Database selected for read: Default')
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'Profiler':
            return db == db_name
        elif app_label == 'Accountant':
            return db == 'default'
        return None
