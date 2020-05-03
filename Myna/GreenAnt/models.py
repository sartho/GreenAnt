
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mongoengine.wtf import model_form

class Ant(db.Document):
    id=db.IntField(required=True)
    email = db.StringField(required=True)
    username=db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)

class Content(db.EmbeddedDocument):
    text = db.StringField()
    lang = db.StringField(max_length=3)

class Post(db.Document):
    author = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=30))
    #content = db.EmbeddedDocumentField(Content)
    content=db.StringField(max_length=250)