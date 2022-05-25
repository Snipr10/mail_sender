# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime

from maria import get_cursor


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    datetime.datetime.now()
    cur = get_cursor()
    cur.execute(
        "SELECT * FROM `prsr_user_mail` WHERE (`mailing_time` >= '23:50' or `mailing_time` < ?)  and `last_mailing` < ?",
        (
            datetime.datetime.now().strftime('%H:%M:%S'),
            (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),)
        )
    for (email) in cur:
        print(f"First Name: {email}, Last Name: {email}")
