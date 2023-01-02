
import psycopg2
import os

#In more complex code I would probably use sqlalchemy.
class Database:
    
    TABLE_NAME = "scrapped_flats"
    
    def __init__(self) -> None:
        self.conn = None
        self.cur = None


    def connect(self):
        database_url = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(database_url)
        self.cur = self.conn.cursor()


    def close(self):
        self.cur.close()
        self.conn.close()


    def create(self):
        self.connect()
        self.cur.execute(f"DROP TABLE IF EXISTS {self.TABLE_NAME}")
        self.cur.execute(f"CREATE TABLE {self.TABLE_NAME} (title TEXT, image_url TEXT, url TEXT)")
        self.conn.commit()
        self.close()
    

    def insert_flats(self, flats):
        self.connect()
        for flat in flats:
            self.cur.execute(f"INSERT INTO {self.TABLE_NAME} (title, image_url, url) VALUES (%s, %s, %s)", (
                flat.get('title'), 
                flat.get('image_url'), 
                flat.get('url')
            ))
        
        self.conn.commit()
        self.close()
    

    def load_flats(self):
        self.connect()
        self.cur.execute(f"SELECT * FROM {self.TABLE_NAME}")
        
        rows = self.cur.fetchall()
        flats = [{
            'title': row[0],
            'image_url': row[1],
            'url': row[2] 
        } for row in rows ]
        
        self.close()
        return flats