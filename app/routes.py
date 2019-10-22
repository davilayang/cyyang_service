from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# from app.food_reviews.getRidgelineData import  getRidgeline
# from app.food_reviews.getStackedAreaData import getStackedArea

from app import app, db
from app.models import Post, Coursework, SkillTree

# Page Managements
## Homepage 
@app.route("/")
def home():
    return """<h1>Hello There! I'm from Flask and for <a href="https://cyyang.me">cyyang.me</a>!<h1>"""

## HTTP errors handling
@app.errorhandler(404)
def not_found(error):
    return """<pre>{}</pre> Error, Page not fonund""".format(error), 404
@app.errorhandler(500)
def server_error(error):
    return """An internal error occurred: <pre>{}</pre> See logs for full stacktrace.""".format(error), 500

# ## Ridgeline Chart
# @app.route('/api/dRidgeline', methods=['GET']) # served at /api/dRidgeline
# def exportRidgeline():
#     start_date = request.args.get('start_date', '')
#     end_date = request.args.get('end_date', '')
#     return getRidgeline(start_date, end_date)

# ## Stacked Area Chart
# @app.route('/api/dStackedArea', methods=['GET']) # served at /api/dStackedArea
# def exportStackedArea():
#     start_date = request.args.get('start_date', '')
#     end_date = request.args.get('end_date', '')
#     return getStackedArea(start_date, end_date)

# Fetch coursework list
@app.route('/courseworks', methods=['GET'])
def view_courseworks():
    tmp = {'Computer Science': [], 'Behavioural Science': [], 'Coursera.com': []}
    cs = db.engine.execute("SELECT * FROM coursework WHERE category = 'Computer Science';")
    bs = db.engine.execute("SELECT * FROM coursework WHERE category = 'Behavioural Science';")
    cr = db.engine.execute("SELECT * FROM coursework WHERE category = 'Coursera.com';")

    for row in cs.fetchall(): tmp['Computer Science'].append(row.coursename) 
    for row in bs: tmp['Behavioural Science'].append(row.coursename) 
    for row in cr: tmp['Coursera.com'].append(row.coursename) 
    return jsonify(tmp)

# Add a new course to list
@app.route('/addcoursework', methods=['POST'])
def add_coursework():
    cat = request.args.get("category")
    name = request.args.get("coursename")
    sql ="""
        INSERT INTO coursework (category, coursename) 
            VALUES('{0}', '{1}')
        """.format(cat, name)

    result = db.engine.execute(sql)
    return jsonify({cat: name}), 200


# Fetch Skill Tree data
@app.route('/skilltree', methods=['GET']) 
def skilltree():
    root = db.engine.execute(\
        "SELECT * FROM skilltree WHERE pid IS NULL;"\
        ).fetchone()
    nodes = db.engine.execute(\
        "SELECT * FROM skilltree WHERE pid IS NOT NULL ORDER BY pid ASC;"\
        ).fetchall()

    # array sorted by pid
    array = [dict(root)] + [dict(node) for node in nodes]
    mapping = {}; tree = []
    # create mapping, w/ node id: index in array
    for idx, node in enumerate(array): 
        mapping[node['id']] = idx
        node['children'] = [] # to append children nodes
    # create tree by append nodes to children array
    for node in array: 
        # if not the root of tree
        if (node['pid'] is not None):
            # find which index is the parent node, append this node to its children array
            array[mapping[node['pid']]]['children'].append(node)
        # if root
        else: 
            tree.append(node)

    return jsonify(tree) # result tree also at array[0]

# Add a new skill to tree
@app.route('/addskill', methods=['POST'])
def add_skill():
    parent = request.args.get("group")
    name = request.args.get("skill")
    
    id = db.engine.execute("SELECT max(id) FROM skilltree").fetchone()[0] + 1
    pid = db.engine.execute(\
        "SELECT id FROM skilltree WHERE name='{}'".format(parent)\
        ).fetchone()[0]
    img = "logo_No-logo.png"
    size = 1000

    sql ="""
        INSERT INTO skilltree (id, pid, name, img, size) 
            VALUES('{0}', '{1}', '{2}', '{3}', '{4}')
        """.format(id, pid, name, img, size)
    result = db.engine.execute(sql)
    return jsonify({parent: name}), 200


# Declaring Flask WTF-Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post_text = StringField('Post_Text', validators=[DataRequired()])

## Test connections with Forms
@app.route('/addpost', methods=['GET', 'POST'])
def add_post():
    postform = PostForm()
    if request.method == 'POST':
        pf = Post(postform.title.data,postform.post_text.data,)
        db.session.add(pf)
        db.session.commit()
        return redirect(url_for('view_posts'))
    return render_template('post_form.html', postform=postform)

@app.route('/posts', methods=['GET', 'POST'])
def view_posts():
    posts = Post.query.all()
    return render_template('view_posts.html', posts=posts)
