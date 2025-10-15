from sms import send_sms
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Send SMS
    send_sms(os.getenv('TWILIO_TO_NUMBER'), "Ahoy 👋", os.getenv('TWILIO_FROM_NUMBER'))


if __name__ == "__main__":
    main()