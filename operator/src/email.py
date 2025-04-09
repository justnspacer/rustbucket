import smtplib
from email.mime.text import MIMEText

sender_email = "your_email@gmail.com"
receiver_email = "[RecipientEmail]"
password = "your_app_password"

# Email content
msg = MIMEText("Hello from Python email!")
msg["Subject"] = "Python Test Email"
msg["From"] = sender_email
msg["To"] = receiver_email

# Sending email using Gmail SMTP
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print("Email sent successfully.")