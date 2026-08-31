import os
import sys
import shutil
import django
from django.core.management import call_command

def run():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    # Reset old SQLite DB for fresh schema application
    db_file = os.path.join(base_dir, 'db.sqlite3')
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print("Reset database for upgraded schema.")
        except Exception as e:
            print(f"DB reset note: {e}")

    # Reset migration folders for accounts, categories, products
    for app in ['accounts', 'categories', 'products']:
        mig_dir = os.path.join(base_dir, 'apps', app, 'migrations')
        if os.path.exists(mig_dir):
            for item in os.listdir(mig_dir):
                if item != '__init__.py' and (item.endswith('.py') or item.endswith('.pyc')):
                    try:
                        os.remove(os.path.join(mig_dir, item))
                    except Exception:
                        pass

    print("--- 1. Making Migrations ---")
    call_command('makemigrations', 'accounts', 'categories', 'products')

    print("--- 2. Applying Migrations ---")
    call_command('migrate')

    print("--- 3. Running Django Test Suite ---")
    call_command('test', 'apps.accounts', 'apps.categories', 'apps.products')

    print("--- 4. Seeding Initial Prototype Data ---")
    call_command('seed_data')

if __name__ == '__main__':
    run()
