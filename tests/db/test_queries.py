import pytest
from pprint import pprint
from typing import Dict, Any
from sqlalchemy.engine.row import Row
from framework.data_base.db_client import DbClient
from dotenv import load_dotenv
import os

load_dotenv()


class TestDbClient(DbClient):

    DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

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
    try:
        # Initializing DbClient
        client = DbClient(url=DATABASE_URL)
        
    except Exception as e:
        # Error while connecting: Check port and creds
        pytest.fail(f"Error while connection: {e}. Check port and creds") 

    TEST_EMAIL = "test_user@example.com"
    TEST_ID = 101 

    exists = client.user_exists(email=TEST_EMAIL, id=TEST_ID)

    user_data = client.get_user_data(email=TEST_EMAIL, id=TEST_ID)
    pretty_print_row(user_data)

    user_data_by_email = client.get_user_data(email="another_user@example.com")
    pretty_print_row(user_data_by_email)

    TIMEOUT = 5 # seconds

    was_created = client.wait_until_user_created(
    email=TEST_EMAIL, 
    id=TEST_ID, 
    timeout=TIMEOUT
    )

    if was_created:
        print(f"User has been created in {TIMEOUT} seconds")
    else:
        print(f"User wasn't found")