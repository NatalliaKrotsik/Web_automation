import pytest
from pprint import pprint
from typing import Dict, Any
from sqlalchemy.engine.row import Row
from framework.data_base.db_client import DbClient

DB_USER = 'db_user'
DB_PASS = 'Pretty_db_pass'
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'api_gateway'

# Creating URL for SQLAlchemy.
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# ----------------------------------

class TestDbClient(DbClient):
    def pretty_print_row(row: Row | None) -> None:
        '''Side function for beautiful printing of Row object.'''
        if row is None:
            print("    -> User not found (None)")
            return
        
    # Creating a dictionary from Row
        columns = ['id', 'email', 'name']
        data: Dict[str, Any] = {}
        for i, col_name in enumerate(columns):
            if i < len(row):
                data[col_name] = row[i]
            
        print("  User's data (SQLAlchemy Row):")
        pprint(data, indent=4)

    def test_execute_db_client_functions_manually():
        """
        Test function to demonstrate DbClient functionality and print outputs to terminal.
        Run via 'poetry run pytest <path_to_this_file>'.
        """
        print("\n" + "="*50)
        print(f"Trying to connect to DB: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        print(f"   URL (without password): {DATABASE_URL.split('@')[0]}@...")

    try:
        # Initializing DbClient
        client = DbClient(url=DATABASE_URL)
        print("DbClient initialized.")
        
    except Exception as e:
        # Error while connecting: Check port and creds
        pytest.fail(f"Error while connection: {e}. Check port and creds") 

    # --- Test data Change for real ---
    TEST_EMAIL = "test_user@example.com"
    TEST_ID = 101 

    print("\n--- 1. Demonstration 'user_exists' ---")
    exists = client.user_exists(email=TEST_EMAIL, id=TEST_ID)
    print(f"User with email '{TEST_EMAIL}' and id '{TEST_ID}' exists? -> **{exists}**")

    
    print("\n--- 2. Demonstration 'get_user_data' ---")

    user_data = client.get_user_data(email=TEST_EMAIL, id=TEST_ID)
    print(f"🔎 Search by email='{TEST_EMAIL}' and id='{TEST_ID}':")
    pretty_print_row(user_data)

    # ADD DATA HERE 
    user_data_by_email = client.get_user_data(email="another_user@example.com")
    print(f"\nSearch by email: another_user@example.com")
    pretty_print_row(user_data_by_email)

    print("\n--- 3. Demonstration 'wait_until_user_created' ---")
    TIMEOUT = 5 # seconds
    print(f"Waiting for user with timeout: {TIMEOUT}s...")

    was_created = client.wait_until_user_created(
    email=TEST_EMAIL, 
    id=TEST_ID, 
    timeout=TIMEOUT
    )

    if was_created:
        print(f"User has been created in {TIMEOUT} seconds")
    else:
        print(f"User wasn't found")

    print("\n" + "="*50)