"""
Anonymous Mode Utility Functions
"""

from flask_login import current_user
from datetime import datetime

def can_see_secret_posts(user):
    """Check if user can see secret posts (moderators and admins only)"""
    if not user or not user.is_authenticated:
        return False
    return user.Role in ['moderator', 'admin']

def get_author_display_name(post, user=None):
    """Get the appropriate display name for a post author"""
    if not post.is_anonymous:
        return post.FirstName
    
    # Check if author should be revealed
    if should_reveal_author(post, user):
        return post.anonymous_author.FirstName if post.anonymous_author else "Unknown"
    
    return "Anonymous User"

def should_reveal_author(post, user=None):
    """Check if the anonymous author should be revealed"""
    if not post.is_anonymous:
        return True
    
    # Check if user is moderator/admin
    if user and can_see_secret_posts(user):
        return True
    
    # Check reveal conditions
    if post.anonymous_reveals:
        for reveal in post.anonymous_reveals:
            if reveal.should_reveal:
                return True
    
    return False

def filter_posts_for_user(posts, user=None):
    """Filter posts based on user permissions"""
    filtered_posts = []
    
    for post in posts:
        # Skip secret posts unless user is moderator/admin
        if post.is_secret and not can_see_secret_posts(user):
            continue
        
        filtered_posts.append(post)
    
    return filtered_posts

def get_anonymous_posts_for_moderator(user):
    """Get all anonymous posts for moderator review"""
    if not can_see_secret_posts(user):
        return []
    
    from .models import Posts
    return Posts.query.filter_by(is_anonymous=True).order_by(Posts.date.desc()).all()

def check_reveal_conditions():
    """Check and update reveal conditions for all posts"""
    from .models import AnonymousReveal
    from website import db
    
    reveals = AnonymousReveal.query.filter_by(is_revealed=False).all()
    
    for reveal in reveals:
        if reveal.should_reveal:
            reveal.is_revealed = True
            reveal.revealed_at = datetime.now()
    
    db.session.commit()

def get_anonymous_stats():
    """Get statistics about anonymous posts"""
    from .models import Posts, AnonymousReveal
    
    total_anonymous = Posts.query.filter_by(is_anonymous=True).count()
    secret_posts = Posts.query.filter_by(is_secret=True).count()
    revealed_posts = AnonymousReveal.query.filter_by(is_revealed=True).count()
    
    return {
        'total_anonymous': total_anonymous,
        'secret_posts': secret_posts,
        'revealed_posts': revealed_posts
    }
