from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import test
from .models import Posts,PostsImg

dm = Blueprint("dm", __name__)

dm.route("")