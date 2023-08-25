import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv("../config/.env")

# Access environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_CLIENT = os.getenv("EMAIL_CLIENT")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")


def send_gmail(subject, message):
    # Create a MIME message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = EMAIL_CLIENT
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Connect to SMTP server and send email
    try:
        smtp_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        smtp_server.starttls()
        smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp_server.sendmail(EMAIL_HOST_USER, EMAIL_CLIENT, msg.as_string())
        smtp_server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", str(e))


def main():
    send_gmail("AlgoTrading - New Crossover ALERT!!", "We found a new crossover.")


if __name__ == "__main__":
    main()
