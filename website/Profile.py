from flask import Blueprint ,render_template,request,flash,redirect,url_for
import re
from .models import User
from flask_login import login_user, login_required,logout_user,current_user
from werkzeug.security import check_password_hash ,generate_password_hash
from . import db
from .models import Posts

Profile = Blueprint('Profile',__name__)

@Profile.route('/Profile')
@login_required
def show_profile():

    posts = Posts.query.filter_by(user_id = current_user.id).all()
    return render_template('Profile.html',user=current_user,posts=posts)
@Profile.route("/delete_account", methods=['GET','POST'])
@login_required
def del_acc():
    
    if request.method == "POST":
        Ver_password = request.form.get("ver-password")
        if not check_password_hash(current_user.password, Ver_password):
            flash("Incorrect password. Please try again.", category="error")
            return render_template("delete_account.html", user=current_user)
        user = User.query.get(current_user.id)
        if user:
            logout_user() 
            db.session.delete(user)
            db.session.commit()
            flash("Your account has been deleted.", category="success")
            return redirect(url_for("auth.login"))
    return render_template("delete_account.html", user=current_user)

@Profile.route("/profile/<int:user_id>")
@login_required
def show_user_profile(user_id):
    user = User.query.get(user_id)
    posts = Posts.query.filter_by(user_id = user_id).all()
    return render_template("user_profile.html", user=user, posts=posts)

@Profile.route('/profile/passwordChange/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    if current_user.id != user_id:
        flash('You are not authorized to change this password.', 'error')
        return redirect(url_for('Profile.show_profile'))
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('Profile.change_password', user_id=user_id))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('Profile.change_password', user_id=user_id))

        if len(new_password) < 7:
            flash('Password must be at least 7 characters long.', 'error')
            return redirect(url_for('Profile.change_password', user_id=user_id))

        user = User.query.get(user_id)
        if user:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('Profile.show_profile'))

    return render_template('change_password.html', user=current_user)