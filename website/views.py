from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Group
from .models import Posts

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    posts = Posts.query.order_by(Posts.date.desc()).all()
    groups = Group.query.all()
    return render_template("home.html", user=current_user, groups=groups,posts=posts)
