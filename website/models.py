from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=False), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # group_id  = db.Column(db.Integer,nullable=True)
    FirstName = db.Column(db.String(150))
    images = db.relationship("PostsImg", backref="post", lazy=True)

class PostsImg(db.Model):
    __tablename__ = "Posts_img"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))
    name = db.Column(db.Text, nullable= False)
    mimetype = db.Column(db.Text,nullable= False)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    FirstName = db.Column(db.String(150))
    Role = db.Column(db.String(50), default="user")
    '''
    posts = db.relationship('Post')
    '''

# table for groups
class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"<Group {self.name}>"

# table for group memberships (users joining groups)
class GroupMember(db.Model):
    __tablename__ = "group_members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), default=func.now())


 