from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.row import Row

class DbClient:
    def __init__(self,url):
        self.engine = create_engine(url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        '''
        echo - use this flag for logging, it will return all sql queries in terminal 
        sessionmaker - creates class Session and we create fabrick of ORM sessions, we automaticly manage transactions and work with objects   
        Do not use commit() function becase it will save all changes in sql table
        Don't use 'self.engine.begin()' in case it will make a commit to data base
        Always use context manager "with" when opening a session so it will close automaticly  
        '''

    def user_exists(self,email:str,id:int) -> bool:
        '''
        This method checks that user exists in data base
        '''
        ...

    def get_user_data(self,email:str,id:int) -> Row | None:
        '''
        This method returns user data from data base as Row object
        Row - object of result string that SQLAlchemy returns when you make a SELECT query
        '''
        ...

    def wait_until_user_created(self,email:str,id:int,timeout:int) -> bool:
        '''
        This method waits for user creation in data base
        '''
        ...