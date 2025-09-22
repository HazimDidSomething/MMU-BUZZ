
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import test
from .models import Posts,test
from datetime import date
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    posts = Posts.query.order_by(Posts.date.desc()).all()
    communities = test.query.all()
    if current_user.reset_time != date.today():
        current_user.votes_remaining = 10
        current_user.reset_time = date.today()
        db.session.commit()
    return render_template("home.html", user=current_user, communities=communities,posts=posts)
@views.route("/ping")
def ping():
    return "pong", 200

@views.route("/community")
@login_required
def community_page():
    communities = test.query.all()
    return render_template("community.html", user=current_user, communities=communities)
