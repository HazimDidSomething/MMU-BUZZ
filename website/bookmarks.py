from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from .models import Bookmark, Posts
from . import db

bookmarks = Blueprint('bookmarks', __name__)

@bookmarks.route('/bookmark/<int:post_id>')
@login_required
def bookmark_post(post_id):
    post = Posts.query.get_or_404(post_id)
    existing_bookmark = Bookmark.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if existing_bookmark:
        db.session.delete(existing_bookmark)
        db.session.commit()
        flash("Bookmark removed!", "success")
    else:
        new_bookmark = Bookmark(user_id=current_user.id, post_id=post_id)
        db.session.add(new_bookmark)
        db.session.commit()
        flash("Post bookmarked!", "success")
    
    return redirect(url_for('post.ViewPost', post_id=post_id))

@bookmarks.route('/bookmarks')
@login_required
def view_bookmarks():
    bookmarked_posts = Posts.query.join(Bookmark).filter(
        Bookmark.user_id == current_user.id
    ).order_by(Bookmark.created_at.desc()).all()
    
    return render_template('bookmarks.html', 
                           user=current_user, 
                           posts=bookmarked_posts,
                           title="My Bookmarks")