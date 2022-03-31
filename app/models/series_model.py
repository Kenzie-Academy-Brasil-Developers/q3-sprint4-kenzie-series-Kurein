from http import HTTPStatus
import psycopg2
import os

DB_HOST= os.getenv("DB_HOST")
DB_NAME= os.getenv("DB_NAME")
DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")

class Series():

    def __init__(self):
        self.fieldnames= ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]

    def open_connection(self):
        self.conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.cur = self.conn.cursor()
        return self.cur
    
    def commit_and_close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def table_init(self):
        cur = self.open_connection()

        cur.execute("""
        create table if not exists ka_series(
	        id BIGSERIAL primary key,
	        serie VARCHAR(100) not null unique,
	        seasons integer not null,
	        released_date date not null,
	        genre VARCHAR(50) not null,
	        imdb_rating float not null
        );
        """)
        
        self.commit_and_close()

    def all_series(self):
        self.table_init()

        cur = self.open_connection()
        cur.execute("SELECT * FROM ka_series")
        db_data = cur.fetchall()

        processed_data = [dict(zip(self.fieldnames, row)) for row in db_data]

        self.commit_and_close()

        return {"data": processed_data}, HTTPStatus.OK

    def get_by_id(self, serie_id):
        cur = self.open_connection()
        query = """
            select * from ka_series
            where
                id = %s;
        """
        cur.execute(query, serie_id)
        serie_data= cur.fetchone()

        self.commit_and_close()

        return dict(zip(self.fieldnames, serie_data)), HTTPStatus.OK

    def create_serie(self, data):
        cur = self.open_connection()

        data["serie"] = data["serie"].title()
        data["genre"] = data["genre"].title()

        serie_values = tuple(data.values())
        query = """
        insert into ka_series
            (serie, seasons, released_date, genre, imdb_rating)
        values
            (%s, %s, %s, %s, %s)
        returning *
        """

        cur.execute(query, serie_values)

        returned_serie = cur.fetchone()

        self.commit_and_close()

        return dict(zip(self.fieldnames, returned_serie)), HTTPStatus.CREATED
