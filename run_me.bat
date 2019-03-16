@echo off
cmd /q /c "cd /d %~dp0\env\Scripts & activate & cd /d %~dp0\UnifiedIT & python manage.py runserver"