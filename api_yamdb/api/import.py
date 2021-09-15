import csv
import sqlite3

con = sqlite3.connect('/Users/maximagarev/Dev/api_yamdb/api_yamdb/db.sqlite3')
cur = con.cursor()

with open('/Users/maximagarev/Dev/api_yamdb/api_yamdb/static/data/users_x.csv','r') as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['username'],  i['email'], i['role'], i['bio'], i['first_name'], i['last_name'], i['password']) for i in dr]

cur.executemany("INSERT INTO main.users_user(id, username, email, role, bio, first_name, last_name, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()