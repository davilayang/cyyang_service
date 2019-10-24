# initial insertions to postgres database, run with: python initDB.py
from app import db
import json

def init_coursework(): 
    # Coursework list, from json to postgres sql
    filePath ="./app/static/data/courseworks.json"
    with open(filePath) as file:
        data = json.load(file)

    # delete everything in the table, and reset primary key
    # find the seq by \d coursework
    db.engine.execute("DELETE FROM coursework;")
    db.engine.execute("ALTER SEQUENCE coursework_id_seq RESTART WITH 1;")

    insertStrings = ""
    for category in data: 
        for coursename in data[category]: 
            insertStrings += "('{0}', '{1}'), ".format(category, coursename)

    results = db.engine.execute(\
    "INSERT INTO coursework ({0}, {1}) VALUES {2};"\
        .format('category', 'coursename', insertStrings[:-2])) 
        # string slicing by :-2 to remove comma at end of string
    return results.rowcount

def init_skilltree(): 
    # Skills list, from json to postgres sql
    filePath ="./app/static/data/skills.json"
    with open(filePath) as file:
        data = json.load(file)

    # delete everything in the table, if there is value
    db.engine.execute("DELETE FROM skilltree;")

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

    results = db.engine.execute(\
    "INSERT INTO skilltree ({0}, {1}, {2}, {3}, {4}) VALUES {5};"\
        .format('id', 'pid', 'name', 'img', 'size', insertStrings[:-2])) 
        # string slicing by :-2 to remove comma at end of string

    return results.rowcount

if __name__ == '__main__':
    print('...init coursework table...')
    rowCount = init_coursework()
    print('inserted {} rows'.format(rowCount))

    print('...init skiltree table...')
    rowCount = init_skilltree()
    print('inserted {} rows'.format(rowCount))
