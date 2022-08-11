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
from telegram import Bot

CHAT_ID = "-748459012"

URL = "https://api.glassen-it.com/component/socparser/content/getReportDocxRef?period=%s&thread_id=%s"
LOGIN_URL = "https://api.glassen-it.com/component/socparser/authorization/login"

EMAIL = 'report@glassen-it.com'
EMAIL_LOGIN = "report"
EMAIL_PASSWORD = "J7sp7b8jf"


def get_now():
    return datetime.datetime.now() + datetime.timedelta(hours=3)


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
    i = BytesIO(report.content)

    file_name = bytes(
        report.headers.get('Content-Disposition').replace("attachment;filename=", "").replace(
            '"', ""), 'latin1').decode('utf-8')
    return i, file_name


def send_message_email(email_to, i, file_name, report_text):
    i.seek(0)
    binary_data = i.read()

    port = 465
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg['Subject'] = 'Автоматическая рассылка отчёта по выбранным субъектам/событиям'
    msg['From'] = EMAIL
    msg['To'] = email_to
    print(email_to)
    # msg.set_content('Добрый день! \n'
    #                 'В соответствии с выбранными вами временным интервалом и объектами мониторинга был'
    #                 f' сформирован отчёт по запросу по следующим субъектам/событиям: \n {report_text}'
    #                 )

    msg.set_content('Добрый день! \n'
                    'Во вложении сформированный отчёт'
                    )

    file_name = "report.docx"
    maintype, _, subtype = (mimetypes.guess_type(file_name)[0] or 'application/octet-stream').partition("/")

    msg.add_attachment(binary_data, maintype=maintype, subtype=subtype, filename=file_name)

    with smtplib.SMTP_SSL("smtp.glassen-it.com", port, context=context) as server:
        server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        server.send_message(msg)

    try:
        BOT.send_document(chat_id=CHAT_ID,
                          document=binary_data,
                          filename=file_name,
                          caption=f"Отчет отправлен {email_to}"
                          )
    except Exception as e:
        print(e)


def send_message_time(id_, uri, time_, email, report_text):
    try:
        print(id_)
        try:
            i, file_name = get_report(uri)

            now_time = get_now()
            print(now_time)
            seconds = now_time.second + now_time.minute * 60 + now_time.hour * 3600
            print(f'sleep time {time_ - seconds}, {id_}')
            if 0 < time_ - seconds < 85800:
                time.sleep(time_ - seconds)
            print(f'sleep time {time_ - seconds}')
        except Exception as e:
            print(e)
        try:
            send_message_email(email.split(), i, file_name, report_text[1:-1])
            new, conn = get_cursor()
            new.execute(
                "UPDATE `prsr_user_mail` SET is_prepare=0, last_mailing=? WHERE id=?", (get_now(), id_,)
            )
            conn.commit()
            conn.close()
        except Exception as e:

            new, conn = get_cursor()
            new.execute(
                "UPDATE `prsr_user_mail` SET is_prepare=0 WHERE id=?", (id_,)
            )
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)


def sends():
    cur, set_conn = get_cursor()
    cur.execute(
        "SELECT id, last_mailing, mailing_time, reference_ids, thread_id, topics, email, period, is_prepare FROM "
        "`prsr_user_mail` WHERE is_prepare=0 and ('00:10:00' >= `mailing_time` or `mailing_time` >= '23:50:00' or ("
        "`mailing_time` >= ? and ? >= `mailing_time`))  and "
        "`last_mailing` < ?",
        (
            (get_now() - datetime.timedelta(minutes=3)).strftime(
                '%H:%M:%S'),
            (get_now() + datetime.timedelta(minutes=3)).strftime(
                '%H:%M:%S'),
            (get_now() - datetime.timedelta(hours=1)).strftime(
                '%Y-%m-%d %H:%M:%S'),)
    )
    new, conn = get_cursor()

    for line in cur:

        new.execute(
            "UPDATE `prsr_user_mail` SET is_prepare=1 WHERE id=?", (line[0],)
        )
        conn.commit()
        reference_ids = ""
        for r in json.loads(line[3]):
            reference_ids += "&reference_ids[]=" + str(r)
        uri = URL % (line[7], line[4]) + reference_ids
        threading.Thread(target=send_message_time, args=(line[0], uri, line[2].seconds, line[6], line[5])).start()
    conn.close()
    set_conn.close()


if __name__ == '__main__':
    SESSION = login(SESSION)
    try:
        BOT = Bot("5400054992:AAEJzk6lQfBnBxVwr4GS4tOafAEuj1Wavxs")
    except Exception as e:
        BOT = None
    print(get_now())
    while True:
        print("step")
        print(get_now())

        try:
            sends()
        except Exception as e:
            print(e)
        time.sleep(1 * 60)
