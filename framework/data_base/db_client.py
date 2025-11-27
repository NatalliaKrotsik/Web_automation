from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

class DbClient:
    def __init__(self,url):
        self.engine = create_engine(url)
        self.connection = self.engine.connect()
        '''
        Don't use 'self.engine.begin()' in case it will make a commit to data base 
        '''

    def select_user_data(self,connection,query):
        with self.engine as engine:
            result = engine.execute(query)
            return f'{result}'
        
def test_db(query = 'SELECT VERSION'):
    result = query.select_user_data()