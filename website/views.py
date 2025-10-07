
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import test
from .models import Posts,test, PostComment, feedback , CommunityMember
from datetime import date
from . import db
import random

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    view_type = request.args.get("view", "all")  # "all", "joined", or "announcements"

    # Get all communities (for right sidebar)
    communities = test.query.all()
    random.shuffle(communities)
    communities = communities[:5]

    # Communities the user joined
    joined_communities = db.session.query(test).join(CommunityMember).filter(
        CommunityMember.user_id == current_user.id
    ).all()

    # Filter posts depending on view_type
    if view_type == "joined":
        if not joined_communities:
            posts = []  # No posts to show
        else:
            community_ids = [c.id for c in joined_communities]
            posts = Posts.query.filter(
                Posts.status == "approved",
                Posts.community_id.in_(community_ids)
            ).order_by(Posts.date.desc()).all()

    elif view_type == "announcements":
        posts = Posts.query.filter_by(status="approved",user_id=1)\
            .order_by(Posts.date.desc()).all()
    else:
        # Default: all approved posts
        posts = Posts.query.filter_by(status="approved")\
            .order_by(Posts.date.desc()).all()

    # Reset daily votes
    if current_user.reset_time != date.today():
        current_user.votes_remaining = 10
        current_user.reset_time = date.today()
        db.session.commit()

    return render_template(
        "home.html",
        user=current_user,
        communities=communities,
        posts=posts,
        joined_communities=joined_communities,
        view_type=view_type
    )

@views.route("/ping")
def ping():
    return "pong", 200

@views.route("/community")
def community_page():
    communities = test.query.all()
    return render_template(
        "viewallcommunity.html",
        user=current_user if current_user.is_authenticated else None,
        communities=communities
    )
