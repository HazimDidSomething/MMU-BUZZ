from flask import Blueprint ,render_template,request,flash,redirect,url_for
import re
from .models import User
from flask_login import login_user, login_required,logout_user,current_user
from werkzeug.security import check_password_hash
from . import db

Profile = Blueprint('profile',__name__)

@Profile.route('/Profile')
def show_profile():
    return render_template('Profile.html',user=current_user)
@Profile.route("/delete_account", methods=['GET','POST'])
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