import random
import pandas as p
import datetime as dt
from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText


def send_mail(receiption, content):

    msg = MIMEText(content, "plain", "utf-8")
    msg['Subject'] = 'Happy Birthday!'
    msg['From'] = "Matthias <>"
    msg['To'] = receiption

    try:
        s = SMTP("cyllene.uberspace.de", port=587)
        s.starttls()
        s.login(user="", password="")
    except SMTPException as e:
        print("Error: unable to send email")
        print(e)
    else:
        s.sendmail("", receiption, msg.as_string())
        print("Successfully sent email")
    finally:
        s.quit()


def prepare_letter(name):

    file_path = f"templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as file:
        content = file.read()

    return content.replace("[NAME]", name)


try:
    data = p.read_csv("birthdays.csv")
except FileNotFoundError:
    data = p.DataFrame()

data["birthday_tupl"] = [(data_row.month, data_row.day)
                         for (index, data_row) in data.iterrows()]

today_tupl = (dt.datetime.now().month, dt.datetime.now().day)
for _, row in data.loc[data["birthday_tupl"] == today_tupl].iterrows():
    send_mail(row.email, prepare_letter(row["name"]))
