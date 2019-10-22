# initial insertions to postgres database, run with: python initDB.py
from app import db
import json

# Coursework list, from json to postgres sql
filePath ="./app/static/data/courseworks.json"
with open(filePath) as file:
    data = json.load(file)

insertStrings = ""
for category in data: 
    for coursename in data[category]: 
        insertStrings += "('{0}', '{1}'), ".format(category, coursename)

db.engine.execute(\
"INSERT INTO coursework ({0}, {1}) VALUES {2}"\
    .format('category', 'coursename', insertStrings[:-2])) 
    # string slicing by :-2 to remove comma at end of string


# Skills list, from json to postgres sql
filePath ="./app/static/data/skills.json"
with open(filePath) as file:
    data = json.load(file)

# flatten the dict to array, w/ [{name, img, size, id, parent_id}]
def flattenJson(node):
    def recursion(node, array=[], idx=0, pidx=None):
        array.append({
            'id': idx, 'pid': pidx, 
            'name': node['name'], 'img': node['img'], 'size': node['size'],
        })
        # if node having children
        if node.get('children'): 
            pidx = idx # current index as parent index
            for child in node.get('children'):
                idx, array = recursion(child, array, idx+1, pidx)
        return idx, array
    return recursion(node)[1]

insertStrings = ""
for row in flattenJson(data): 
    tmp = 'NULL' if row['pid'] is None else row['pid'] # NULL as missing for SQL
    insertStrings += "({0}, {1}, '{2}', '{3}', {4}), "\
        .format(row['id'], tmp, row['name'], row['img'], row['size'])

db.engine.execute(\
"INSERT INTO skilltree ({0}, {1}, {2}, {3}, {4}) VALUES {5}"\
    .format('id', 'pid', 'name', 'img', 'size', insertStrings[:-2])) 
    # string slicing by :-2 to remove comma at end of string
