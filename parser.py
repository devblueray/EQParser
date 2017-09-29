import re
import json
import sqlite3
from flask import Flask, request,render_template

app=Flask(__name__)

conn = sqlite3.connect('skybank.sqlite3')
c = conn.cursor()
c.execute("drop table if exists skybank;")
c.execute("create table skybank(key text, value integer, character text);")
c.execute("drop table if exists requests;")
items = {}
banks = []
files = ['iltar-bank', 'boop-bank']

def insertItems(file):
    with open(file, 'r') as file:
      for line in file:
        if not re.match(r'^\s*$', line):
          line = line.strip('\n').split('\t')
          if line[1] != "Empty" and line[0].startswith("Bank"):
            if items.get(line[1]) == None:
              print("Value: " + 1*line[3])
              items[line[1]] = [(1*int(line[3])),[]]
              print(type(line[3]))
            else:
              items[line[1]][0] += int(line[3])
            if file.name.partition("-")[0] not in items[line[1]][1]:
                    items[line[1]][1].append(file.name.partition("-")[0])


def newInsertItems(*args):
    for file in args:
        print(file)
        with open(file, 'r') as current:
            for line in current:
                if not re.match(r'^\s*$', line):
                    line = line.strip('\n').split('\t')
                    if line[1] != "Empty" and line[0].startswith("Bank"):
                        if items.get(line[1]) == None:
                            items[line[1]] = [{"Hi":2}] #must have this for now, it inits the list/dict(will try to fix later)
                            items[line[1]][0]=({current.name:line[3]})
                        else:
                            items[line[1]][0].update({current.name:line[3]})
    print(items)
    
    #print("TEST", items['Backpack'])                           
newInsertItems(*files)
#for item in items:
#    data = []
#    data.append(item)
#    data.append(items[item][0])
#    strTmp = ""
 #   for fname in items[item][1]:
 #       strTmp += fname + " "
 #   data.append(strTmp)
    
    #print("{}: Count: {} File: {}".format(item, items[item][0], strTmp))
#    c.execute('''insert into skybank(key,value,character) values(?,?,?);''',(data))
conn.commit()

print("DATABASE")
a = c.execute("select * from skybank;").fetchall()
@app.route('/')
def index():
    return render_template('item_list.html', items=a)

if __name__ == "__main__":
    app.run()
