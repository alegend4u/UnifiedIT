import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from UnifiedIT import settings

DB_ENGINE = 'django.db.backends.postgresql'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'

DB_SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database_settings')


def save_to_file(db_settings):
    db_string = """
DATABASES['%(NAME)s'] = {
'ENGINE': '%(ENGINE)s',
'NAME': '%(NAME)s',    
'USER': '%(USER)s',    
'PASSWORD': '%(PASSWORD)s', 
'HOST': '%(HOST)s',         
'PORT': '%(PORT)s',         
} """ % db_settings

    db_file = os.path.join(DB_SETTINGS_PATH, db_settings['NAME'] + '.py')

    # Writing settings to file
    with open(db_file, 'w') as f:
        f.write(db_string)


def delete_file(name):
    db_file = os.path.join(DB_SETTINGS_PATH, name + '.py')
    os.remove(db_file)


class DBManager:
    def __init__(self, db_name):
        self.name = db_name

    def create(self):
        con = None
        cur = None
        try:
            con = psycopg2.connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cur = con.cursor()
            cur.execute('CREATE DATABASE "{}" ;'.format(self.name))

            print("New Database created for", self.name)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Cannot create database for {}: {}".format(self.name, error))
        finally:
            cur.close()
            con.close()

        new_database = {'ENGINE': DB_ENGINE, 'NAME': self.name, 'USER': DB_USER, 'PASSWORD': DB_PASSWORD,
                        'HOST': DB_HOST, 'PORT': DB_PORT}

        # Modify Settings.py accordingly
        settings.DATABASES[self.name] = new_database  # Using username to define each database uniquely.

        # Save the new settings for new DB to file
        save_to_file(new_database)

        # Migration on the database
        os.chdir(settings.BASE_DIR)
        os.system('python manage.py migrate --database='+self.name)

        return new_database

    def delete(self):
        con = None
        cur = None
        try:
            con = psycopg2.connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cur = con.cursor()

            cur.execute('DROP DATABASE "{}" ;'.format(self.name))
            print("DATABASE DELETED! - ", self.name)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Database Error occurred!: ", error)
            cur.close()
            con.close()
        try:
            delete_file(self.name)
        except FileNotFoundError as error:
            print("Database file not found!", error)

        # if settings.DATABASES.get(self.name):
        #     del settings.DATABASES[self.name]
        print(settings.DATABASES)
        print('Account {} deleted!', self.name)
