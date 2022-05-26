# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import threading
import time
from email.message import EmailMessage
from io import BytesIO
import datetime
import smtplib, ssl
import mimetypes

import requests as requests

from maria import get_cursor

URL = "https://api.glassen-it.com/component/socparser/content/getReportDocxRef?period=%s&thread_id=%s"
LOGIN_URL = "https://api.glassen-it.com/component/socparser/authorization/login"

SESSION = requests.session()
EMAIL = 'report@glassen-it.com'
EMAIL_LOGIN = "report"
EMAIL_PASSWORD = "J7sp7b8jf"


def login(session):
    payload = {
        "login": "java_api",
        "password": "4yEcwVnjEH7D"
    }
    response = session.post(LOGIN_URL, json=payload)
    if not response.ok:
        raise Exception("can not login")
    return session


def get_report(uri):
    report = SESSION.get(uri)
    i = BytesIO(report.content)
    file_name = bytes(
        report.headers.get('Content-Disposition').replace("attachment;filename=", "").replace(
            '"', ""), 'latin1').decode('utf-8')
    return i, file_name


def send_message_email(email_to, file, file_name, report_text):
    port = 465
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg['Subject'] = 'Автоматическая рассылка отчёта по выбранным субъектам/событиям'
    msg['From'] = EMAIL
    msg['To'] = email_to

    file.seek(0)
    binary_data = file.read()
    maintype, _, subtype = (mimetypes.guess_type(file_name)[0] or 'application/octet-stream').partition("/")
    print(f"maintype {maintype}")
    print(f"subtype {subtype}")
    print(f"file_name {file_name}")

    msg.set_content('Добрый день! \n'
                    'В соответствии с выбранными вами временным интервалом и объектами мониторинга был'
                    f' сформирован отчёт по запросу по следующим субъектам/событиям: \n{report_text}'
                    )
    msg.add_attachment(binary_data, maintype=maintype, subtype=subtype, filename=file_name)
    print("smtplib login")

    with smtplib.SMTP_SSL("smtp.glassen-it.com", port, context=context) as server:
        print("try login")

        server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        print("sucess login")
        server.send_message(msg)
        print("send")


def send_message_time(id_, uri, time_, email, report_text):
    try:

        i, file_name = get_report(uri)
        print("send_message_time")
        now_time = datetime.datetime.now()
        seconds = now_time.second + now_time.minute*60 + now_time.hour*3600
        print(seconds-time_)
        if time_-seconds > 0:
            time.sleep(time_-seconds)
        try:
            print("send_message_time")

            send_message_email(email, i, file_name, "report_text")
            new, conn = get_cursor()
            new.execute(
                    "UPDATE `prsr_user_mail` SET is_prepare=0, last_mailing=? WHERE id=?", (datetime.datetime.now(), id_, )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


def sends():
    datetime.datetime.now()
    cur, set_conn = get_cursor()
    cur.execute(
        "SELECT id, last_mailing, mailing_time, reference_ids, thread_id, topics, email, period, is_prepare FROM `prsr_user_mail` WHERE is_prepare=0 and (`mailing_time` >= '23:50' or `mailing_time` >= ?)  and `last_mailing` < ?",
        (
            (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime('%H:%M:%S'),
            (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),)
    )
    # for id, last_mailing, mailing_time, reference_ids, thread_id, topics, email, period, is_prepare) in cur:
    new, conn = get_cursor()

    for line in cur:
        print(line)
        print(line)
        print(f"First Name: {line[0]}, Last Name: {line[0]}")

        new.execute(
            "UPDATE `prsr_user_mail` SET is_prepare=1 WHERE id=?", (line[0],)
        )
        conn.commit()
        reference_ids = ""
        for r in json.loads(line[3]):
            reference_ids += "&reference_ids[]=" + str(r)
        uri = URL % (line[7], line[4]) + reference_ids
        print(uri)
        threading.Thread(target=send_message_time, args=(line[0], uri, line[2].seconds, line[6], line[5])).start()
    conn.close()
    set_conn.close()
# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    SESSION = login(SESSION)
    sends()