#author : Hanbyul (Estrella) Kim
#estrellakim03@gmail.com
#chatgpt helped a bit for locating further errors :D
#install smtplib for this


import smtplib
from email.mime.text import MIMEText


SENDER_GMAIL = "sample@gmail.com" # Replace with your email address

#This is the google app password
#https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j
#Check the above stackoverflow on how to get the google app password
GOOGLE_APP_PASSWORD = "zocouuajtpnfoygm"  # Replace with your app password

SUBJECT = ""    #Name subject
FROM = "EGlow"
RECEIVER_GMAIL = []
TEXTFILE = "receiver_emails.txt"    #name of the txt file

MESSAGE = """
THIS IS A TEST
"""

msg = MIMEText(MESSAGE)
msg['Subject'] = SUBJECT
msg['From'] = FROM

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER_GMAIL, GOOGLE_APP_PASSWORD)

    with open(TEXTFILE) as f:
        RECEIVER_GMAIL.extend(f.readlines())

    for receiver in RECEIVER_GMAIL:
        receiver = receiver.strip()
        if receiver:
            msg['To'] = receiver
            server.send_message(msg)
            print(f"Email sent to {receiver}")
        else:
            print("Invalid email address")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    server.quit()