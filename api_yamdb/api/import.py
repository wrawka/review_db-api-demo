import csv
import sqlite3

con = sqlite3.connect('/Users/maximagarev/Dev/api_yamdb/api_yamdb/db.sqlite3')
cur = con.cursor()

with open('/Users/maximagarev/Dev/api_yamdb/api_yamdb/static/data/category.csv','r') as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['name'],  i['slug']) for i in dr]

cur.executemany("INSERT INTO main.reviews_category(id, name, slug) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()