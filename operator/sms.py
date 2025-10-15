import os
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')


def send_sms(to_number, message_body, from_number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    messaging_service_sid=os.getenv('TWILIO_MESSAGING_SERVICE_SID'),
        body=message_body,
        to=to_number,
        from_=from_number
    )
    print(message.sid)