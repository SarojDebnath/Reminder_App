from flask_mail import Message
from . import mail
import smtplib

def send_email_reminder(email, name, due_date):
    # Create SMTP session
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Login with your email and password
    server.login('iwilllive.agoodlife97@gmail.com', 'tcpv jnyn nyqe kxaq')
    subject = "Muscle Garage"
    body = f"Hi {name}, your gym subscription is due on {due_date}. Please make the payment."
    message = f'Subject: {subject}\n\n{body}'
    # Sending the mail
    server.sendmail('iwilllive.agoodlife97@gmail.com', email, message)
    print('Mail Sent')
    server.quit()

