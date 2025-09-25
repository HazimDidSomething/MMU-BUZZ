from flask import Blueprint ,render_template,request,flash,redirect,url_for,session
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from . import db
from .utils.mailer import send_otp_email
import random

signUP = Blueprint('signUP',__name__)

@signUP.route('/sign-up',methods=['GET', 'POST'])
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
            flash('Please use your MMU email (e.g. name@student.mmu.edu.my or name@mmu.edu.my)', category='error')
        

        elif len(FirstName) < 2:
            flash('UR NAME IS TOO SHORT.',category='error')
            
        elif Passowrd1 != Password2:
            flash('Passwords dont match.',category='error')
            
        elif len(Passowrd1) < 7:
            flash('PASSWORD IS TOO SHORT IT SHOULD BE MORE THAN 7 CHARATERS.',category='error')
            
        else:
            otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
            session['signup_info'] = {
                'email': email,
                'FirstName': FirstName,
                'password': generate_password_hash(Passowrd1, method='pbkdf2:sha256'),
            }
            session['otp'] = otp
            send_otp_email(email, otp)
            flash('An OTP has been sent to your email. Please verify to complete registration. It might take some time to send.', category = 'success')
            return redirect(url_for('signUP.verify_otp'))

    return render_template("sign_up.html",user = current_user)

@signUP.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('otp') :
            flash('OTP verified successfully!', category='success')
            user_data = session.get('signup_info')
            if user_data:
                new_user = User(
                    email=user_data['email'],
                    FirstName=user_data['FirstName'],
                    password=user_data['password'],
                    Role='user'
                )
                db.session.add(new_user)
                db.session.commit()
                session.pop('signup_info', None)
                session.pop('otp', None)
                flash('Account created successfully! You can now log in.', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Session expired. Please sign up again.', category='error')
                return redirect(url_for('sign_up_otp.sign_up'))      
        else:       
            flash('Invalid OTP. Please try again.', category='error')

    return render_template('verify_otp.html', user=current_user)
