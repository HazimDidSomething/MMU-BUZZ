from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date
from datetime import date

class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=False), default=func.now())
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    FirstName = db.Column(db.String(150))
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=True)
    status = db.Column(db.String(50), default="approved")
    reasons = db.Column(db.String(10000), nullable=True)
    flair_id = db.Column(db.Integer, db.ForeignKey('community_flairs.id', ondelete='SET NULL'), nullable=True)

    images = db.relationship("PostsImg", backref="post", lazy=True,cascade="all, delete-orphan")
    community = db.relationship("test", backref="posts", lazy=True)

class PostsImg(db.Model):
    __tablename__ = "Posts_img"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id',ondelete="CASCADE"))
    public_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.Text, nullable= False)
    mimetype = db.Column(db.Text,nullable= False)

class PostComment(db.Model):
    __tablename__ = "Posts_comment"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id',ondelete="CASCADE"))
    content = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    Firstname = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=False), default=func.now())
    user = db.relationship("User", backref="comments")
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    FirstName = db.Column(db.String(150))
    Role = db.Column(db.String(50), default="user")
    votes_remaining = db.Column(db.Integer, default=10)
    reset_time = db.Column(db.Date,default=lambda: date.today())
    posts = db.relationship("Posts", backref="author", cascade="all, delete-orphan")
    otp = db.Column(db.String(6), nullable=True)
    # Karma economy
    karma = db.Column(db.Integer, default=0)
    last_login_date = db.Column(db.Date, nullable=True)
    login_streak = db.Column(db.Integer, default=0)
    
    # Badge relationship
    badges = db.relationship("Badge", secondary="user_badges", back_populates="users")

    @property
    def badge(self):
        if self.karma >= 2500:
            return "Elder"
        if self.karma >= 1500:
            return "Legend"
        if self.karma >= 1000:
            return "Novice"
        if self.karma >= 500:
            return "Elite"
        if self.karma >= 100:
            return "Rising Star"
        return None

    @property
    def flair_unlocked(self):
        return self.karma >= 500


# table for communities
class test(db.Model):
    __tablename__ = "communities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    members = db.relationship(
        "CommunityMember",
        backref="community",
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"<Communities {self.name}>"

# table for communities memberships 
class CommunityMember(db.Model):
    __tablename__ = "communities_members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id", ondelete="CASCADE"), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), default=func.now())
    community_role = db.Column(db.String(50), default="member")
    
    

class feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    Firstname = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=False), default=func.now())
    user = db.relationship("User", backref="feedbacks")

# Bookmark model
class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    user = db.relationship("User", backref="bookmarks")
    post = db.relationship("Posts", backref="bookmarks")

# Community Flair model
class CommunityFlair(db.Model):
    __tablename__ = "community_flairs"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), server_default='#6c757d', nullable=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    community = db.relationship("test", backref="flairs")
    posts = db.relationship("Posts", backref="flair")

# Badge model
class Badge(db.Model):
    __tablename__ = "badges"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    icon = db.Column(db.String(50), nullable=True)  # Bootstrap icon class
    color = db.Column(db.String(20), server_default='#6c757d', nullable=True)
    karma_threshold = db.Column(db.Integer, nullable=True)  # Auto-awarded at karma milestones
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # Many-to-many relationship with users
    users = db.relationship("User", secondary="user_badges", back_populates="badges")

# Junction table for user badges
user_badges = db.Table('user_badges',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badges.id', ondelete='CASCADE'), primary_key=True),
    db.Column('earned_at', db.DateTime(timezone=True), server_default=func.now())
)  