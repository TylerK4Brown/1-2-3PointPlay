import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env and injects into os.environ

# Set up the email information from the environment variables
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

# Set up the email message
msg = MIMEMultipart("alternative")
msg["From"] = formataddr(("1-2-3 Point Play", GMAIL_USER))
msg["To"] = "firegate0@gmail.com"
msg["Subject"] = "🏈 1-2-3 Point Play: Quick test of a different header"

# Display the email contents in HTML
html_text = """
<h1>
    The 1-2-3 Point Play season has begun! <br>
</h1>
<h2>
    <a href="https://1-2-3pointplay-preseason.streamlit.app/">Visit the website here!</a>
</h2>
"""

# Attach the HTML content to the email message
msg.attach(MIMEText(html_text, "html"))

# Send the email using Gmail's SMTP server
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, "firegate0@gmail.com", msg.as_string())