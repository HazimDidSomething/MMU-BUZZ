from flask import Blueprint ,render_template,request,flash,redirect,url_for,jsonify
from sqlalchemy import inspect
from . import db
from flask_login import login_user, login_required,logout_user,current_user
from .models import User


DBinfo = Blueprint('DBinfo',__name__)

@DBinfo.route('/DB_INFO')
def show_db_info():
    # Get all users
    users = User.query.all()

    # Build dictionary with details
    user_data = []
    for u in users:
        user_data.append({
            "id": u.id,
            "email": u.email,
            "name": u.FirstName,
            "password": u.password
        })

    return jsonify({"users": user_data})