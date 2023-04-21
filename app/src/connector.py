import mysql.connector
import pandas
import numpy

class Connector():
    def __init__(self, host, user, pwd, database):
        self.host = host
        self.user = user
        self.pwd = pwd 
        if database:
            self.database = database
            self.db = mysql.connector.connect(host = self.host, user = self.user, passwd = self.pwd, database = self.database)
        else:
            self.database = ""
            self.db = mysql.connector.connect(host = self.host, user = self.user, passwd = self.pwd)
    
    def cursor(self):
        self.cursor = self.db.cursor()
        
    def createDatabase(self, name):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + name)
    
    def showAllDatabases(self):
        self.cursor.execute("SHOW DATABASES")
        
        print("DATABASES")
        for db in self.cursor:
            print(db)
            
    def createTable(self, name, content):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(name, content))
    
    def showAllTables(self):
        self.cursor.execute("SHOW TABLES")
        
        print("TABLES")
        for tb in self.cursor:
            print(tb)
        
    def insertTable(self, table, col, content, ignore=False):
        if ignore:
            self.cursor.execute("INSERT IGNORE INTO {} ({}) VALUES {}".format(table, ",".join(col), content))
        else:
            self.cursor.execute("INSERT INTO {} ({}) VALUES {}".format(table, ",".join(col), content))
        self.commit()
    
    def insertMultipleTable(self, table, content):
        self.cursor.executemany(self.sqlFormula, content)
        self.commit()
        
    def selectTable(self, table, selection):
        self.cursor.execute("SELECT {} FROM {}".format(selection, table))
        return self.cursor.fetchall()
    
    def updateTable(self, table, col_update, content_update, col, content):
        #print("UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(table, col_update, content_update, col, content))
        self.cursor.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(table, col_update, content_update, col, content))
        self.commit()
    
    def deleteRow(self, table, col, content):
        self.cursor.execute("DELETE FROM {} WHERE {} = '{}'".format(table, col, content))      
        self.commit()
        
    def deleteTable(self, table):
        self.cursor.execute("DROP TABLE IF EXISTS {}".format(table))      
        self.commit()
    
    def commit(self):
        self.db.commit()
        
    def close(self):
        self.db.close()

