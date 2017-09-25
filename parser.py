import re
import json
import sqlite3
from flask import Flask, request,render_template

app=Flask(__name__)

conn = sqlite3.connect('skybank.sqlite3')
c = conn.cursor()
c.execute("drop table if exists skybank;")
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
              items[line[1]] = [1,[]]
              
            else:
              items[line[1]][0] += 1
            #print(line[1])
            #print(items[line[1]][1])
            if file.name.partition("-")[0] not in items[line[1]][1]:
                    items[line[1]][1].append(file.name.partition("-")[0])

for file in files:
    insertItems(file)
for item in items:
    data = []
    data.append(item)
    data.append(items[item][0])
    strTmp = ""
    for fname in items[item][1]:
        strTmp += fname + " "
    print ("thing: " + strTmp)
    data.append(strTmp)
    print(data)
    
    print("{}: Count: {} File: {}".format(item, items[item][0], strTmp))
    c.execute('''insert into skybank(key,value,character) values(?,?,?);''',(data))
conn.commit()

print("DATABASE")
a = c.execute("select * from skybank;").fetchall()
print (a)
print (type(a))
@app.route('/')
def index():
    return render_template('item_list.html', items=a)

if __name__ == "__main__":
    app.run()
