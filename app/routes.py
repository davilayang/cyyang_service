from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.food_reviews.getRidgelineData import  getRidgeline
from app.food_reviews.getStackedAreaData import getStackedArea

from app import app, db
from app.models import Post, Book

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

## Ridgeline Chart
@app.route('/api/dRidgeline', methods=['GET']) # served at /api/dRidgeline
def exportRidgeline():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    return getRidgeline(start_date, end_date)

## Stacked Area Chart
@app.route('/api/dStackedArea', methods=['GET']) # served at /api/dStackedArea
def exportStackedArea():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    return getStackedArea(start_date, end_date)


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
