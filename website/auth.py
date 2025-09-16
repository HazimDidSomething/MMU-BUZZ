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

@auth.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('MMU-email')
        FirstName = request.form.get('FirstName')
        Passowrd1 = request.form.get('Password1')
        Password2 = request.form.get('Password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('USER ALREADY EXIST', category='error')
        elif len(email) < 4 :
            flash("Your email is too short." , category='error')

        elif not re.match(r'^[\w\.-]+@(student\.)?mmu\.edu\.my$', email):
            flash('Please use your MMU email (e.g. name@student.mmu.edu.my)', category='error')
        elif len(FirstName) < 2:
            flash('UR NAME IS TOO SHORT.',category='error')
            
        elif Passowrd1 != Password2:
            flash('Passwords dont match.',category='error')
            
        elif len(Passowrd1) < 7:
            flash('PASSWORD IS TOO SHORT IT SHOULD BE MORE THAN 7 CHARATERS.',category='error')
            
        else:
            new_user = User(email = email, FirstName = FirstName, password = generate_password_hash(Passowrd1, method ='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account Created!', category='success')
            return redirect(url_for('auth.login'))
            #add user data to data base

    return render_template("sign_up.html",user = current_user)


