import re
import json
import sqlite3
from collections import defaultdict
from flask import Flask, request,render_template
import MySQLdb

app=Flask(__name__)

db = MySQLdb.connect(host="localhost",
        user="root",
        passwd="abc123",
        db="inventory")
cursor = db.cursor()

items = {}
banks = []
files = ['iltar-bank', 'boop-bank']

def newInsertItems(*args):
  print(args)
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

def dbInsertItems(*args):
  print(args)
  for file in args:
    with open(file, 'r') as current:
      inventory = [line.strip('\n').split('\t') for line in current]
      for item in inventory:
        if (re.match('Bank[0-9]-', item[0])):
          if (not re.match('Empty', item[1])):
            #if item[1] not in items:
            items[item[1]] = {file: item[3]}
            item_name = item[1].replace("'","\\'")
            print("{}, {}, {}".format(item, item[3], file))
            sql1="INSERT INTO items(item) VALUES ('{}')".format(item_name)
            sql2="INSERT INTO banks(bank,count,item) VALUES('{}',{},'{}')".format(file,item[3],item_name)
            cursor.execute(sql1)
            cursor.execute(sql2)
  db.commit()
  db.close()
  return item

inventory = dbInsertItems(*files)
#dynamo = dict_to_item(inventory)
dynamo = json.dumps(inventory)
print(type(inventory))
print(dynamo)
cursor.close()
@app.route('/')
def index():
    return render_template('item_list.html', items=a)

#if __name__ == "__main__":
#    app.run()
