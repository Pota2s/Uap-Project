import sqlite3 as sql

con = sql.connect("db.sqlite3")

cur = con.cursor()

res = cur.execute("SELECT * FROM sqlite_master")
for i in res.fetchall():
    print(i)

res = cur.execute("SELECT name,id FROM store_store")
for i in res.fetchall():
    print(i)