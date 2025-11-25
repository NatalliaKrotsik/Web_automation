from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

class DbClient:
    def __init__(self,url):
        self.engine = create_engine(url)
        self.Sessoin = sessionmaker(bind=self.engine)

    def fetch_one(self, query):
        '''
        Creates session and automatically closes it
        Executes SQL or SQLAlchemy query
        Fetches only one result row
        Returns Row object or None
        '''
        with self.Sessoin() as session:
            result = session.execute(query).fetchone()
            return result 
        
    def fetch_all(self, query):
        '''
        Creates session and automatically closes it
        Executes SQL or SQLAlchemy query
        Fetches all result rows
        Returns list of Row objects (empty list if no results)
        '''
        with self.Sessoin() as session:
            result = session.execute(query).fetchall()
            return result 
        
    def execute(self, query): 
        '''
        Creates session and automatically closes it
        Executes SQL or SQLAlchemy query that modifies data (INSERT, UPDATE, DELETE)
        Commits transaction
        Returns None
        '''
        with self.Session() as session: 
            session.execute(query) 
            session.commit()