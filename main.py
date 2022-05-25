# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import threading

from maria import get_cursor





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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    datetime.datetime.now()
    cur = get_cursor()
    cur.execute(
        "SELECT id, last_mailing, mailing_time, reference_ids, thread_id, topics, email, period, is_prepare FROM `prsr_user_mail` WHERE is_prepare=0 and (`mailing_time` >= '23:50' or `mailing_time` >= ?)  and `last_mailing` < ?",
        (
            (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime('%H:%M:%S'),
            (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),)
        )
    # for id, last_mailing, mailing_time, reference_ids, thread_id, topics, email, period, is_prepare) in cur:
    for line in cur:

        print(f"First Name: {line[0]}, Last Name: {line[0]}")
        cur.execute(
            "UPDATE `prsr_user_mail` set is_prepare=1 WHERE id=?", (line[0],)
        )
        # threading.Thread(target=send_message_time, args=(uri, time, int(d[0]), d[4])).start()
