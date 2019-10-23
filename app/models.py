# database models/tables
from app import app, db

# model for coursework list
# id, category, courseName
class Coursework(db.Model):
    __tablename__ = 'coursework'

    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(80))
    coursename = db.Column(db.String(255))

    def __init__(self, category, courseName):
        self.category = category
        self.coursename = coursename


# tree structure to database
# https://makandracards.com/makandra/45275-storing-trees-in-databases

# Parent Association
class SkillTree(db.Model):
    __tablename__ = 'skilltree'

    id = db.Column(db.Integer(), primary_key=True)
    pid = db.Column(db.Integer()) # parent node id
    name = db.Column(db.String(80)) # skill name
    img = db.Column(db.String(80)) # logo image file name
    size = db.Column(db.Integer()) # size of logo

    def __init__(self, id ,pid, name, img, size):
        self.id = id 
        self.pid = pid
        self.name = name
        self.img = img
        self.size = size
