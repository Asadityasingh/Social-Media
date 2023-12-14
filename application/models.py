from .database import db
from flask_login import UserMixin

class User (db.Model,UserMixin):
        __tablename__="user"
        id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String,nullable=False)
        password = db.Column(db.String,nullable=False)
        keys = db.Column(db.String,nullable=False)

        name=db.Column(db.String,nullable=False)
        age=db.Column(db.Integer, nullable=False)
        address=db.Column(db.String,nullable=False)
        about=db.Column(db.String,nullable=False)
        email=db.Column(db.String,nullable=False)
        dp= db.Column(db.Text)
        

#model for img table
class Img(db.Model):
        user_name = db.Column(db.String,nullable=False)
        img_Id=db.Column(db.Integer, primary_key=True)
        # img = db.Column(db.Text,unique=True, nullable=False)
        img_name = db.Column(db.Text, nullable=False)
        mimetype = db.Column(db.Text, nullable=False)
        ct = db.Column(db.Text)
        caption = db.Column(db.Text)
        title= db.Column(db.Text)


class Following(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String,nullable=False)
        following=db.Column(db.Text)

class Follower(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String,nullable=False)
        followers=db.Column(db.Text)