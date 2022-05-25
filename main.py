# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json
import threading

from maria import get_cursor

URL = "https://api.glassen-it.com/component/socparser/content/getReportDocxRef?period=%s&thread_id=%s"




def send_message_time(uri, time_, chat_id, report_text):
    try:
        print(uri)
        print(time_)
        i, file_name = get_report(uri)
        sleep_time = (time_ - get_time_now()).seconds + 5
        if sleep_time > 0:
            time.sleep(sleep_time)
        print("send" + str(uri))
        # TODO send email
        try:
            updater.bot.send_document(chat_id=chat_id,
                                      document=i,
                                      filename=file_name,
                                      caption=report_text
                                      )
        except Exception:
            pass
        try:
            send_message_email(get_mail(chat_id), i, file_name, report_text)
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
        print(f"First Name: {line[0]}, Last Name: {line[0]}")

        new.execute(
            "UPDATE `prsr_user_mail` SET is_prepare=1 WHERE id=?", (line[0],)
        )
        conn.commit()

        uri = URL % (line[7], line[4])
        print(uri)
        str_ = "reference_ids[]".join(str(x) for x in json.loads("[1,2,3,4]"))
        print(str_)
        # threading.Thread(target=send_message_time, args=(uri, time, int(d[0]), d[4])).start()
    conn.close()
    set_conn.close()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sends()