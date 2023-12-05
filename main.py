import requests
from bs4 import BeautifulSoup
import unicodedata
import smtplib
from email.mime.text import MIMEText
import json
from datetime import datetime
from time import sleep

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent")

def get_email_body():
    perfect_north_url = "https://perfectnorth.com/snow-report/"
    soup = BeautifulSoup(requests.post(perfect_north_url).content, "lxml")
    message = soup.find("div", {"class":"col-sm-12"}).text.strip()
    cleaned_message = unicodedata.normalize("NFKD",message)

    cleaned_message_lines=[]
    message_lines = cleaned_message.split("\n")
    for line in message_lines:
        if line.strip()!="":
            cleaned_message_lines.append(line)

    return "\n\n".join(cleaned_message_lines)

def IsItTime(desired_time):
    now = datetime.now()
    if (now.hour == desired_time["hour"]) and (now.minute == desired_time["minute"]):
        return True
    return False

time_to_run = {"hour":12, "minute":45}

if __name__=="__main__":

    while True:

        with open("secrets.json") as my_file:
            secrets = json.load(my_file)

        subject = "Perfect North Daily Update"
        body = get_email_body()
        sender = secrets["sender_email"]
        recipients = secrets["recipients"]
        password = secrets["sender_email_password"]

        send_email(
            subject=subject,
            body=body,
            sender=sender,
            recipients=recipients,
            password=password
        )

        sleep(61)

        while IsItTime(time_to_run) != True:
            sleep(30)
