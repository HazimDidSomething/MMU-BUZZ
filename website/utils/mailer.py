import smtplib
from email.mime.text import MIMEText
from flask import render_template
from flask_login import current_user
import os


def send_otp_email(to_email, otp):
    
    SMTP_SERVER = os.getenv("MAIL_SERVER") 
    SMTP_PORT = 587
    SMTP_USER = os.getenv("MAIL_USERNAME")
    SMTP_PASS = os.getenv("MAIL_PASSWORD")    

    from_email = os.getenv("MAIL_DEFAULT_SENDER")
    to_email = to_email
    subject = 'MMU BUZZ OTP Email'
    body = f"""Hello! WELCOME TO MMU BUZZ. Your OTP is: {otp}. Please do not share it with anyone.
    Have a great day! If you did not request this, please ignore this email thank you."""


    # Create the email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

# Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully!")
        return render_template('verify_otp.html', user=current_user)
    except Exception as e:
        return render_template('sign_up.html', user=current_user)
        
    finally:
        return render_template('sign_up.html', user=current_user)
