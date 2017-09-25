import re
import json
import sqlite3
from flask import Flask, request,render_template

app=Flask(__name__)

conn = sqlite3.connect('skybank.sqlite3')
c = conn.cursor()
c.execute("drop table if exists  skybank;")
c.execute("create table skybank(key text, value integer, character text);")
items = {}
files = ['iltar-bank', 'boop-bank']

def insertItems(file):
    with open(file, 'r') as file:
      for line in file:
        if not re.match(r'^\s*$', line):
          line = line.strip('\n').split('\t')
          if line[1] != "Empty" and line[0].startswith("Bank"):
            if items.get(line[1]) == None:
              items[line[1]] = [1,file.name]
              
            else:
              items[line[1]][0] += 1

for file in files:
    insertItems(file)
for item in items:
    print("{}: Count: {} File: {}".format(item, items[item][0], items[item][1]))
#c.executemany("insert into skybank values(?,?,?);", items.items())
conn.commit()

a = c.execute("select * from skybank;").fetchall()

@app.route('/')
def index():
    return render_template('item_list.html', items=items)

if __name__ == "__main__":
    app.run()
