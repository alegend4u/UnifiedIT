# Important for editing the DATABASES variable
from UnifiedIT.settings import DATABASES
from Accountant.db_creator import DB_SETTINGS_PATH
import os

# Load all the accounts' database settings
for file in os.listdir(DB_SETTINGS_PATH):
    if file == 'desktop.ini':
        continue
    full_path = os.path.join(DB_SETTINGS_PATH, file)
    f = open(full_path)
    content = f.read()
    f.close()

    # you'd better be sure that the file doesn't contain anything malicious
    exec(content)
