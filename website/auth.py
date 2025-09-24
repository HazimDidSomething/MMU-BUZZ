from flask import Blueprint ,render_template,request,flash,redirect,url_for
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user,current_user

from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('MMU-email')
        password = request.form.get('Password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('LOGGED IN ' , category='success')
                login_user(user,remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password' , category='error')
        else:
            flash('user dont exist' , category='error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




