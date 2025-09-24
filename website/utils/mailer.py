import smtplib
from email.mime.text import MIMEText
import os
import dotenv   
dotenv.load_dotenv()

# Brevo (Sendinblue) SMTP settings
SMTP_SERVER = os.getenv("MAIL_SERVER")
SMTP_PORT = os.getenv("MAIL_PORT")
SMTP_LOGIN = os.getenv("MAIL_USERNAME")  
SMTP_PASSWORD = os.getenv("MAIL_PASSWORD")
FROM_EMAIL = os.getenv("MAIL_FROM")


def send_verification_email(to_email, otp):
    subject = "Verify your MMU-Buzz account"
    body = f"Your verification code is: {otp}"

    msg = MIMEText(body)
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        print(f"ent OTP email to {to_email}")
    except Exception as e:
        print(f" Failed to send email: {e}")