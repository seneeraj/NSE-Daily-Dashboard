import smtplib
from email.message import EmailMessage
from config import *

def send_email_with_attachment():
    msg = EmailMessage()
    msg['Subject'] = "Daily NSE Derivatives Dashboard"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("Attached is your Daily Derivatives Dashboard.")

    with open("dashboard_report.png", "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='png', filename="dashboard.png")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        print("Email sent!")