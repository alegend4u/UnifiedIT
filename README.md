## An Institute Management System built using Multi-tenant Architecture!
Complete Manual Under Construction!

### Instructions for running the project
1. Download the project.
2. Install Django or activate an environment having Django 3.0.3 or higher.
3. Open terminal inside the downloaded project and run the following command:

    `python manage.py migrate --database=admin_db`
    
    This will make the admin database ready.
4. Let's create a superuser in our newly created database.

    `python manage.py createsuperuser --database=admin_db`
    
5. Now start the server:

    `python manage.py runserver`
    
6. Go to `localhost:8000` to make an account request.
7. Go to `localhost:8000/admin` and login with superuser credentials and click `Account Requests`.
8. Select the request and select `Grant selected requests` in actions dropdown menu and click go.
    This will create the account and its separate database for the requested institute.
9. The newly created account can be logged in with request username and password as 'ins_admin'. (Will be generated randomly and sent to the provided email address once the request is approved).
10. The further functionalities are designed but are currently in implementation phase.
