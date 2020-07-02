# Important for editing the DATABASES variable
import json
from pathlib import Path

from Accountant.db_manager import DB_CONFS_DIR
from UnifiedIT import settings

# Load all the accounts' database settings

confs_dir = Path(DB_CONFS_DIR)

if not confs_dir.exists():
    confs_dir.mkdir(parents=True)

for file in confs_dir.glob('*.json'):
    with open(str(file)) as f:
        content = json.load(f)
    db_key = file.with_suffix('').name  # account_db_name
    settings.DATABASES[db_key] = content
