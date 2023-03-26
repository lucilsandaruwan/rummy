from models.dbConnector import DBConnector
class Model:
    con = None
    cur = None

    def __init__(self):
        self.con = DBConnector.get_db()
        self.cur = self.con.cursor()
    
    def close_db(self):
        DBConnector.close_db()