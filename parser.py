import re
import json
import sqlite3
from collections import defaultdict
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

def newInsertItems(*args):
  for file in args:
    with open(file, 'r') as current:
      inventory = [line.strip('\n').split('\t') for line in current]
      for item in inventory:
        if (re.match('Bank[0-9]-', item[0])):
          if (not re.match('Empty', item[1])):
            if item[1] not in items:
              items[item[1]] = {file: item[3]}
            else:
              items[item[1]].update({file: item[3]})
    return items
    
inventory = newInsertItems(*files)
print(inventory)
@app.route('/')
def index():
    return render_template('item_list.html', items=a)

#if __name__ == "__main__":
#    app.run()
