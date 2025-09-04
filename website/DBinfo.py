from flask import Blueprint ,render_template,request,flash,redirect,url_for,jsonify
from . import db
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
            "password": u.password,
            "Role": u.Role
        })

    return jsonify({"users": user_data})