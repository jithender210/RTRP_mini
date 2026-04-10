import sqlite3

conn=sqlite3.connect('database.db')
cursor=conn.cursor()
 
cursor.execute('''SELECT * FROM categories''')
categories=cursor.fetchall()
print(categories)