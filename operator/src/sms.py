from twilio.rest import Client
account_sid = '[AccountSID]'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)
message = client.messages.create(
  messaging_service_sid='[MessagingServiceSID]',
  body='Ahoy 👋',
  to='+...' # Replace with your phone number
)
print(message.sid)