# from flask_migrate import Migrate, MigrateCommand

# TODO:
# 1. instead of using Pandas, using basic modules to read and upload data
# 2. get cli.command to work with arguments, e.g. flask seed coureswork/ flask seed skilltree
# 3. typing, lint, docstring

import json
from pandas import read_csv
from flask.cli import FlaskGroup
from app.models import app, db, Coursework, SkillTree

cli = FlaskGroup(app)

# command to reset all tables
@cli.command("reset_db") # flask reset_db
def create_db():
    db.drop_all() # drop all tables
    db.create_all() # create all tables
    db.session.commit() # commit all changes

# register another command, to add new row to table
@cli.command("seed_db")
def seed_db():
    db.session.add(Coursework(category="TEST", coursename="SOME-COURSE"))
    db.session.commit()

# register seed_all command to seed all tables
@cli.command("seed_all")
def seed_all():
    print('seeding coursework data', flush=True)
    insert_coursework_data()

    print('seeding skilltree data', flush=True)
    insert_skilltree_data()

    print('seeding food_reviews data', flush=True)
    insert_foodreviews_data()
    return 


# register seed_coursework command
@cli.command("seed_coursework") 
def seed_coursework():
    result = insert_coursework_data()
    return result.rowcount

# register seed_skilltree command
@cli.command("seed_skilltree") 
def seed_skilltree():
    result = insert_skilltree_data()
    return result.rowcount

@cli.command("seed_foodreviews") 
def seed_foodreviews():
    insert_foodreviews_data()
    return 


def insert_coursework_data():

    """
    insert_coursework_data

    Function to reset coursework table and then insert new rows of data 
    into postgresql databse

    """

    with open(f"{app.static_folder}/data/courseworks.json" ) as file: 
        data = json.load(file)

    # prepare data into rows of strings
    insertStrings = ""
    for category in data: 
        for coursename in data[category]: 
            insertStrings += f"('{category}', '{coursename}'), "

    # reset table
    result = db.engine.execute("DELETE FROM coursework;")
    result = db.engine.execute("ALTER SEQUENCE coursework_id_seq RESTART WITH 1;")

    # insert into table
    results = db.engine.execute(
        f"""
        INSERT INTO coursework (category, coursename) 
        VALUES {insertStrings[:-2]};
        """
        # [:-2] to remove comma at end of string
    )

    return result

# flatten the dict to array, w/ [{name, img, size, id, parent_id}]
def flattenJson(node):

    """
    flattenJson

    Function to flatten a nested structured jason string into rows for 
    database insertion

    """

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


def insert_skilltree_data(): 

    """
    insert_skilltree_data

    Function to reset skilltree table and then insert new rows of data 
    into postgresql databse

    """

    with open(f"{app.static_folder}/data/skills.json" ) as file: 
        data = json.load(file)

    insertStrings = ""
    for row in flattenJson(data): 
        tmp = 'NULL' if row['pid'] is None else row['pid'] # NULL for SQL
        insertStrings += f"({row['id']}, {tmp}, '{row['name']}', '{row['img']}', {row['size']}), "

    # reset table
    result = db.engine.execute("DELETE FROM skilltree;")
    
    # insert into table
    result = db.engine.execute(
        f"""
        INSERT INTO skilltree (id, pid, name, img, size) 
        VALUES {insertStrings[:-2]};
        """
    )

    return result


def insert_foodreviews_data():

    """
    insert_foodreviews_data

    Function to reset food_reviews table and then insert new rows of data 
    into postgresql databse

    TODO: 
        - update the function using non-pandas approach
        - i.e. custom functions/classes

    """
    dtypes = {
        'customer_id': 'object', 
        'product_parent': 'object', 
        'star_rating': 'Int64', 
        'helpful_votes': 'Int64', 
        'total_votes': 'Int64', 
        'code': 'object'
    }

    df = read_csv(
        f"{app.static_folder}/data/merged_amz-off_3.csv.gz", 
        compression='gzip', 
        dtype=dtypes,
        parse_dates=['review_date']
    )

    # df.review_date = pd.to_datetime(df.review_date)
    # Insert dataframe to database, as food_reviews table
    df.to_sql(\
        name="food_reviews", if_exists='replace', schema='public', 
        index=False, con=db.engine
        )
    # Alter review_id as primary key
    db.engine.execute("ALTER TABLE food_reviews ADD PRIMARY KEY (review_id);")

    return None

if __name__ == "__main__":
    cli()