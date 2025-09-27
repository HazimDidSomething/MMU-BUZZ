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
    
    # Anonymous mode fields
    is_anonymous = db.Column(db.Boolean, default=False, nullable=False)
    anonymous_author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reveal_date = db.Column(db.DateTime(timezone=True), nullable=True)
    is_secret = db.Column(db.Boolean, default=False, nullable=False)

    images = db.relationship("PostsImg", backref="post", lazy=True,cascade="all, delete-orphan")
    community = db.relationship("test", backref="posts", lazy=True)
    anonymous_author = db.relationship("User", foreign_keys=[anonymous_author_id], backref="anonymous_posts")
    
    # Anonymous polls relationship
    anonymous_poll = db.relationship("AnonymousPoll", backref="post", uselist=False, cascade="all, delete-orphan")
    anonymous_reveals = db.relationship("AnonymousReveal", backref="post", lazy=True, cascade="all, delete-orphan")

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
    
    # Anonymous mode fields
    is_anonymous = db.Column(db.Boolean, default=False, nullable=False)
    anonymous_author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    user = db.relationship("User", backref="comments")
    anonymous_author = db.relationship("User", foreign_keys=[anonymous_author_id], backref="anonymous_comments")
    

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

# Anonymous Poll model
class AnonymousPoll(db.Model):
    __tablename__ = "anonymous_polls"
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id', ondelete='CASCADE'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    options = db.Column(db.JSON, nullable=False)  # List of poll options
    is_multiple_choice = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    votes = db.relationship("AnonymousPollVote", backref="poll", lazy=True, cascade="all, delete-orphan")
    
    @property
    def is_expired(self):
        if not self.expires_at:
            return False
        from datetime import datetime
        return datetime.now() > self.expires_at
    
    @property
    def total_votes(self):
        return len(self.votes)
    
    @property
    def results(self):
        """Calculate poll results with vote counts per option"""
        results = {}
        for option in self.options:
            results[option] = 0
        
        for vote in self.votes:
            for selected_option in vote.selected_options:
                if selected_option in results:
                    results[selected_option] += 1
        
        return results

# Anonymous Poll Vote model
class AnonymousPollVote(db.Model):
    __tablename__ = "anonymous_poll_votes"
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('anonymous_polls.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)  # Nullable for truly anonymous votes
    selected_options = db.Column(db.JSON, nullable=False)  # List of selected options
    voted_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    ip_hash = db.Column(db.String(64), nullable=True)  # For anonymous vote tracking
    
    user = db.relationship("User", backref="poll_votes")

# Anonymous Reveal model for time-delayed reveals
class AnonymousReveal(db.Model):
    __tablename__ = "anonymous_reveals"
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id', ondelete='CASCADE'), nullable=False)
    reveal_type = db.Column(db.String(50), nullable=False)  # 'time_delayed', 'moderator_approved', 'community_vote'
    scheduled_reveal_date = db.Column(db.DateTime(timezone=True), nullable=True)
    reveal_condition = db.Column(db.JSON, nullable=True)  # Store conditions like vote threshold
    is_revealed = db.Column(db.Boolean, default=False, nullable=False)
    revealed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    @property
    def should_reveal(self):
        """Check if the reveal condition has been met"""
        from datetime import datetime
        
        if self.is_revealed:
            return False
            
        if self.reveal_type == 'time_delayed':
            return self.scheduled_reveal_date and datetime.now() >= self.scheduled_reveal_date
        
        elif self.reveal_type == 'moderator_approved':
            return False  # Requires manual moderator action
        
        elif self.reveal_type == 'community_vote':
            if not self.reveal_condition:
                return False
            vote_threshold = self.reveal_condition.get('vote_threshold', 0)
            return self.post.vote >= vote_threshold
        
        return False  