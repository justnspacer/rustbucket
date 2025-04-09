from sms import send_sms
from email import send_email

def main():
    # Send SMS
    send_sms("+0987654321", "Hello via SMS!")

    # Send Email
    send_email("recipient@example.com", "Hello via Email", "This email is sent from Python.")

if __name__ == "__main__":
    main()