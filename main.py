# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import random

import threading
import time
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from io import BytesIO
import datetime
import smtplib, ssl
import mimetypes

import requests as requests

from maria import get_cursor

URL = "https://api.glassen-it.com/component/socparser/content/getReportDocxRef?period=%s&thread_id=%s"
LOGIN_URL = "https://api.glassen-it.com/component/socparser/authorization/login"


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

SESSION = login(requests.session())


def get_report(uri):
    report = SESSION.get(uri)
    s = random.randint(0, 100)
    i = BytesIO(report.content)
    name = f'test{s}.docx'
    open(name, 'wb').write(report.content)
    print(f"name = {name}")
    file_name = bytes(
        report.headers.get('Content-Disposition').replace("attachment;filename=", "").replace(
            '"', ""), 'latin1').decode('utf-8')
    return i, name


def send_message_email(email_to, binary_data, file_name, report_text):
    port = 465
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg['Subject'] = 'Автоматическая рассылка отчёта по выбранным субъектам/событиям'
    msg['From'] = EMAIL
    msg['To'] = email_to

    msg.set_content('Добрый день! \n'
                    'В соответствии с выбранными вами временным интервалом и объектами мониторинга был'
                    f' сформирован отчёт по запросу по следующим субъектам/событиям: \n{report_text}'
                    )

    with open(file_name, "rb") as fp:
        msg.add_attachment(
            fp.read(), maintype="file", subtype="docx", filename="report.docx")


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
        i.seek(0)
        binary_data = i.read()
        now_time = datetime.datetime.now()
        seconds = now_time.second + now_time.minute*60 + now_time.hour*3600
        if time_-seconds > 0:
            time.sleep(time_-seconds)
        try:
            send_message_email(str(email), binary_data, file_name, "report_text")
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
    # #
    # # msg = MIMEMultipart()
    # # fromaddr = 'SENDER EMAIL ADDRESS'
    # # toaddr = 'RECIPIENT EMAIL ADDRESS'
    # # # i, file_name = get_report(
    # # #     "https://api.glassen-it.com/component/socparser/content/getReportDocxRef?period=day&thread_id=5284&reference_ids[]=1180&reference_ids[]=1184"
    # # # )
    # # # i.seek(0)
    # # # i = i.read()
    # # # the_book = SESSION.get("https://api.glassen-it.com/component/socparser/content/getReportDocxRef?period=day&thread_id=5284&reference_ids[]=1180&reference_ids[]=1184", stream=True)
    # # # with open("1.docx", 'wb') as f:
    # # #   for chunk in the_book.iter_content(1024 * 1024 * 2):  # 2 MB chunks
    # # #     f.write(chunk)
    # # # send_message_email("gusevoleg96@gmail.com", i, file_name, "report_text")
    # # #
    # port = 465
    # context = ssl.create_default_context()
    # #
    # msg = EmailMessage()
    # msg['Subject'] = 'Автоматическая рассылка отчёта по выбранным субъектам/событиям'
    # msg['From'] = EMAIL
    # msg['To'] = "gusevoleg96@gmail.com"
    #
    # msg.set_content("Hello, victim!")
    #
    # with open("report.docx", "rb") as fp:
    #     msg.add_attachment(
    #         fp.read(), maintype="file", subtype="docx", filename="report.docx")
    #
    # with smtplib.SMTP_SSL("smtp.glassen-it.com", port, context=context) as server:
    #     print("try login")
    #
    #     server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    #     print("sucess login")
    #     server.send_message(msg)
    #     print("send")
    #

    sends()