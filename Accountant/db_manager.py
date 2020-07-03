import json
import os
from pathlib import Path

from django.core import management

from UnifiedIT import settings

DB_CONFS_DIR = Path('Accountant/account_db_confs')
SQLITE_DIR = Path('Accountant/sqlite_dbs')
with open('Accountant/db_control_conf.json') as f:
    CONTROL_CONF = json.load(f)


def get_db_creator(vendor):
    if vendor == 'postgres':
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        def create(account_db_name, control_conf):
            dbname = control_conf.get('NAME')
            user = control_conf.get('USER')
            password = control_conf.get('PASSWORD')
            host = control_conf.get('HOST')
            port = control_conf.get('PORT')

            if None in [dbname, host, user, password, port]:
                return None

            # Create the database
            con, cur = None, None
            try:
                con = psycopg2.connect(dbname=dbname, host=host, user=user, password=password, port=port)
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

                cur = con.cursor()
                cur.execute('CREATE DATABASE "{}" ;'.format(account_db_name))

                print("New Database created for", account_db_name)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Cannot create database for {}: {}".format(account_db_name, error))
                return None
            finally:
                if con is not None:
                    cur.close()
                if con is not None:
                    con.close()

            # Create and return the account's db conf upon success
            account_db_conf = control_conf.copy()
            account_db_conf['NAME'] = account_db_name
            # TODO: Change other conf parameters for account dbs.

            return account_db_conf

        return create
    if vendor == 'sqlite':
        import sqlite3

        def create(account_db_name, control_conf=None):

            # Set the dbname upon the provided account_db_name
            dbpath = SQLITE_DIR / account_db_name  # Example: ../../CompanyA_db.sqlite3
            account_db_conf = control_conf.copy()
            account_db_conf['NAME'] = str(dbpath)

            # Create the Database
            con = None
            try:
                con = sqlite3.connect(dbpath)
            except sqlite3.Error as sqlite_error:
                print(sqlite_error)
                return None
            finally:
                if con:
                    con.close()
            return account_db_conf

        return create


def get_db_deletor(vendor):
    if vendor == 'postgres':
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        def delete(target_db_name, control_conf):
            dbname = control_conf.get('NAME')
            user = control_conf.get('USER')
            password = control_conf.get('PASSWORD')
            host = control_conf.get('HOST')
            port = control_conf.get('PORT')

            if None in [dbname, host, user, password, port]:
                return False

            con, cur = None, None
            try:
                con = psycopg2.connect(dbname=dbname, host=host, user=user, password=password, port=port)
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

                cur = con.cursor()
                cur.execute('DROP DATABASE "{}" ;'.format(target_db_name))
                print("DATABASE DELETED! - ", dbname)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return False
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()
            return True

        return delete
    if vendor == 'sqlite':
        def delete(target_db_name, control_conf=None):
            dbpath = SQLITE_DIR / target_db_name
            if dbpath.exists():
                os.remove(dbpath)
            return True

        return delete


class DBManager:
    def __init__(self, db_name, vendor=settings.DEFAULT_DB_VENDOR):
        self.name = db_name

        self.conf = None
        self.vendor = None

        # Check if the account already exists and load its conf if it does.
        file = (DB_CONFS_DIR / db_name).with_suffix('.json')
        if file.exists():
            with open(str(file)) as f:
                self.conf = json.load(f)
        else:
            self.conf = CONTROL_CONF[vendor].copy()

        # Assign vendor as per engine
        for vendor in settings.DB_VENDORS:
            if vendor in self.conf['ENGINE']:
                self.vendor = vendor
                break

        # Get creator and deletor for vendor
        self.creator = get_db_creator(self.vendor)
        self.deletor = get_db_deletor(self.vendor)

    def create(self):
        self.conf = self.creator(self.name, self.conf)

        if self.conf is None:
            print('-' * 10, "Database Creation Failed", '-' * 10)
            return False

        # Add to settings.DATABASES with provided name as key
        settings.DATABASES[self.name] = self.conf

        # Save the new settings for new DB to file
        filename = self.name + '.json'
        conf_file = DB_CONFS_DIR / filename
        with open(conf_file, 'w') as write_file:
            json.dump(self.conf, write_file, indent=2)

        # Apply Migrations on the newly created database
        management.call_command('migrate', '--database=' + self.name)

        return self.conf

    def delete(self):
        # Delete the database
        delete_status = self.deletor(self.name, self.conf)
        if not delete_status:
            # This happens mostly because the target db is in other use.
            print(f"[WARNING]: The database {self.name} was not deleted due to some issue. Below is its conf:")
            print(json.dumps(self.conf, indent=2))

        # Delete the account's conf file
        filename = self.name + '.json'
        conf_file = DB_CONFS_DIR / filename
        try:
            os.remove(conf_file)
        except FileNotFoundError as error:
            print(conf_file, ':', error)

        # Delete from settings.DATABASES
        del settings.DATABASES[self.name]

        print('Account {} deleted!', self.name)
