import mysql.connector
 
class Database():
    def __init__(self):
        self.db= mysql.connector.connect(user='root',password='antlstk1@',port='3306',host='localhost',database='managerdb')        
        self.cursor= self.db.cursor() 
    
    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
    
    def executemany(self, query, args):
        self.cursor.executemany(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()
