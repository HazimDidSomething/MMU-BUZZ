
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import test
from .models import Posts, test
from datetime import date
from . import db
from .utils.anonymous import filter_posts_for_user, check_reveal_conditions
import random

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    communities = test.query.all()
    random.shuffle(communities)
    communities = communities[:5]

    # Check and update reveal conditions
    check_reveal_conditions()
    
    posts = Posts.query.filter_by(status="approved").order_by(Posts.date.desc()).all()
    # Filter posts based on user permissions
    posts = filter_posts_for_user(posts, current_user)
    
    if current_user.reset_time != date.today():
        current_user.votes_remaining = 10
        current_user.reset_time = date.today()
        db.session.commit()
    return render_template("home.html", user=current_user, communities=communities,posts=posts)
@views.route("/ping")
def ping():
    return "pong", 200

@views.route("/community")
def community_page():
    communities = test.query.all()
    return render_template(
        "ViewAllCommunity.html",
        user=current_user if current_user.is_authenticated else None,
        communities=communities
    )

@views.route("/zoom-demo")
def zoom_demo():
    return render_template("zoom_demo.html")

@views.route("/anonymous-demo")
def anonymous_demo():
    return render_template("anonymous_demo.html")

@views.route("/anonymous-moderator")
@login_required
def anonymous_moderator():
    from .utils.anonymous import get_anonymous_posts_for_moderator, get_anonymous_stats
    
    # Check if user is moderator
    if current_user.Role not in ['moderator', 'admin']:
        flash("Access denied. Moderator privileges required.", "error")
        return redirect(url_for("views.home"))
    
    secret_posts = get_anonymous_posts_for_moderator(current_user)
    stats = get_anonymous_stats()
    
    # Get pending reveals
    try:
        from . import models
        AnonymousReveal = getattr(models, 'AnonymousReveal', None)
        if AnonymousReveal:
            pending_reveals = AnonymousReveal.query.filter_by(is_revealed=False).order_by(AnonymousReveal.created_at.desc()).all()
        else:
            pending_reveals = []
    except (ImportError, AttributeError):
        # Fallback if AnonymousReveal is not available (migration not run yet)
        pending_reveals = []
    
    return render_template("anonymous_moderator.html", 
                         secret_posts=secret_posts, 
                         stats=stats, 
                         pending_reveals=pending_reveals)