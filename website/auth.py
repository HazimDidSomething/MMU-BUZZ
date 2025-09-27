from flask import Blueprint ,render_template,request,flash,redirect,url_for
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user,current_user

from . import db
from .utils.karma import record_login_streak

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
                # Daily login streak and +1 karma/day
                badges_awarded = record_login_streak(user)
                if badges_awarded:
                    flash(f"🏆 Earned badges: {', '.join(badges_awarded)}", "success")
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




