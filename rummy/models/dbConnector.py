from flask import g
import sqlite3

class DBConnector:
    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    @staticmethod
    def get_db():
        db = sqlite3.connect('../data/rummy.db')
        db.row_factory = DBConnector.dict_factory
        return db
        # if 'db' not in g:
        #     g.db = sqlite3.connect('../data/rummy.db')
        #     g.db.row_factory = DBConnector.dict_factory
        # return g.db
    @staticmethod    
    def close_db():
        db = g.pop('db', None)
        if db is not None:
            db.close()