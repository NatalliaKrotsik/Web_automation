from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.row import Row
import time
import logging
import os 
import framework.utils.utils as helpers

class DbClient:
    """
        DbClient — a class for interacting with a database using SQLAlchemy Core.

        Features:
            - Connects to the database using a provided URL.
            - Automatically loads the schema of the 'users' table.
            - Built-in logger that writes logs both to a file and to the console.
            - Methods for checking user existence, retrieving user data, and waiting for a user to be created.

        Attributes:
            engine (Engine): SQLAlchemy Engine for database connection.
            Session (sessionmaker): SQLAlchemy session factory.
            metadata (MetaData): Database metadata object.
            users (Table): SQLAlchemy Table object representing the 'users' table.
            logger (Logger): Logger instance for debugging and tracking operations.
    """
    def __init__(self,url):
        """
        Initializes the DbClient.

        Args:
            url (str): Database connection URL (e.g., postgresql://user:pass@host/db).

        Initializes:
            - SQLAlchemy Engine
            - Session factory
            - Metadata
            - 'users' table object
            - Logger (writes to console and file)
        """      
        self.logger = logging.getLogger("DbClientLogger")
        self.logger.setLevel(logging.DEBUG)

        root_dir = helpers.get_root_dir()
        log_dir = os.path.join(root_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "dbclient.log")

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.engine = create_engine(url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(bind=self.engine)

        self.users = Table(
            'users', self.metadata,
            Column('id', Integer, primary_key=True), 
            Column('email', String),
            Column('name', String),
            autoload_with=self.engine
        )
        self.logger.debug('DbClient initialized and table "users" loaded')


    def user_exists(self,email:str,id:int, limit=1) -> bool:
        """
        Checks whether a user exists in the database.

        Args:
            email (str): User's email address.
            id (int): User's ID.

        Returns:
            bool: True if the user exists, False otherwise.

        Notes:
            Uses `SELECT id FROM users WHERE email=? AND id=? LIMIT 1`.
            The LIMIT 1 ensures only one row is fetched for efficiency.
            Logs the result of the check.
        """
        query = select(self.users.c.id).where(
            (self.users.c.email == email) & (self.users.c.id == id)
            ).limit(limit)

        with self.Session as session:
            result = session.execute(query)
            exists = result.first() is not None
            self.logger.debug(f"user_exists(email={email}, id={id}) -> {exists}")
            return exists

    def get_user_data(self,email:str,id:int) -> Row | None:
        """
        Retrieves user data from the database as a Row object.

        Args:
            email (str): User's email address.
            id (int): User's ID.

        Returns:
            Row | None: SQLAlchemy Row object with user data if found, None otherwise.

        Notes:
            - Logs whether the user was found or not.
            - Use the returned Row to access columns like row['id'], row['email'], etc.
        """
        query = select(self.users).where(
            (self.users.c.email == email) & (self.users.c.id == id)
        )
        with self.Session as session :
            row = session.execute(query).first()
            if row is not None:
                self.logger.debug(f"User with email={email} and id={id} created")
            else:
                 self.logger.debug(f"User with email={email} and id={id} doesn't exist in data base")
            return row

    def wait_until_user_created(self,email:str,id:int,timeout:int=30) -> bool:
        """
        Waits until a user is created in the database or until a timeout is reached.

        Args:
            email (str): User's email address.
            id (int): User's ID.
            timeout (int, optional): Maximum time to wait in seconds. Default is 30.

        Returns:
            bool: True if the user is created within the timeout, False otherwise.

        Notes:
            - Checks for user existence every 1 second.
            - Logs each check and whether the timeout was reached.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.user_exists(email, id):
                self.logger.debug(f"User with email={email} and id={id} created")
                return True 
            time.sleep(1)

        self.logger.debug(f"Timeout reached: user with email={email} and id={id} doesn't exist in data base")
        return False