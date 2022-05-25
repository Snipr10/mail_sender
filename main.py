# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from maria import get_cursor


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cur = get_cursor()
    cur.execute(
        "SELECT * FROM `prsr_user_mail` WHERE `last_mailing` > '2022-05-24 08:43:54"
        )
    for (email) in cur:
        print(f"First Name: {email}, Last Name: {email}")
