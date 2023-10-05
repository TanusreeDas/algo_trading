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


def send_gmail(log, subject, message):
    # Create a MIME message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = EMAIL_CLIENT
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    # Connect to SMTP server and send email
    try:
        smtp_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        smtp_server.starttls()
        smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp_server.sendmail(EMAIL_HOST_USER, EMAIL_CLIENT, msg.as_string())
        smtp_server.quit()
        log.debug("send_gmail() method executed successfully.")
        print(
            "Email sent successfully!"
        )  # added only to view the message in console,can be deleted.
    except Exception as e:
        log.exception(
            f"An error occurred while sending email from send_email.send_gmail(): %s", e
        )
        log.error("This is a generic Exception block in send_email.send_gmail()")
