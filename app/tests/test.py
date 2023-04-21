import os 
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/') ))

from connector import Connector

conn = Connector("localhost", "root", "AVEave2021!", "test")
conn.cursor()
conn.createDatabase('test')
conn.createTable("students", "name VARCHAR(255), age INTEGER(10)")

conn.showAllDatabases()
conn.showAllTables()

conn.addFormula("INSERT INTO students (name, age) VALUES (%s, %s)")
conn.insertTable(("Kevin", 22))
#conn.insertMultipleTable([("Ben", 21), ("John", 20), ("Karen", 24), ("Peter", 19)])
#conn.deleteRow('students', 'name', 'Kevin')

#conn.deleteTable('students')

#conn.commit()

