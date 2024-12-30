import smtplib
from email.mime.text import MIMEText

# SMTP server configuration
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
USERNAME = 'info@guatemalachurch.com'
PASSWORD = 'Lucas1220!'  # Use your App Password here

from_addr = 'info@guatemalachurch.com'
to_addr = 'mitchell.munoz127@gmail.com'  # Replace with your email address

msg = MIMEText('Test email body')
msg['Subject'] = 'Test Email'
msg['From'] = from_addr
msg['To'] = to_addr

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(from_addr, to_addr, msg.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {str(e)}")
