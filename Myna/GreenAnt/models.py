
from Myna import md
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_mongoengine.wtf import model_form

class Ant(md.Document):
    id=md.IntField(required=True)
    email = md.StringField(required=True)
    username=md.StringField(required=True)
    first_name = md.StringField(max_length=50)
    last_name = md.StringField(max_length=50)

class Content(md.EmbeddedDocument):
    text = md.StringField()
    lang = md.StringField(max_length=3)

class Post(md.Document):
    author = md.ReferenceField(Ant)
    #tags = db.ListField(db.StringField(max_length=30))
    content=md.StringField(max_length=250)