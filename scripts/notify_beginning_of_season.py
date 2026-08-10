import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()  # reads .env and injects into os.environ

my_phone = os.environ["MY_PHONE"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
phone_number = os.environ["TWILIO_NUMBER"]

client = Client(account_sid, auth_token)
client.messages.create(
    to=my_phone,
    from_=os.environ["TWILIO_NUMBER"],
    body=""" 
        🏈 The 1-2-3 Point Play season has officially begun! 🏈
        
        https://1-2-3pointplay-preseason.streamlit.app/
    """
)

