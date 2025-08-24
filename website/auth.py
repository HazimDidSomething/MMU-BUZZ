from flask import Blueprint ,render_template,request,flash
import re

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET', 'POST'])
def login():

    return render_template("login.html",boolean = True)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('MMU-email')
        FirstName = request.form.get('FirstName')
        Passowrd1 = request.form.get('Password1')
        Password2 = request.form.get('Password2')
        if len(email) < 4 :
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
            flash('Account Created!', category='success')
            #add user data to data base

    return render_template("sign_up.html")


