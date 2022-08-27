import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from email.message import EmailMessage
import ssl
import smtplib

RATE_TO_SELL = 4.28


GMAIL_SECRET_KEY = "GMAIL_SECRET_KEY"
# EMAIL_PASSWORD = os.environ.get(GMAIL_SECRET_KEY)
APP_ADMIN_EMAIL = "YOU_EMAIL"
APP_ADMIN_EMAIL2 = "YOUR_EMAIL"
recipient = "RECIPIENT_EMAIL"
FUBON_EXCHANGE_RATE_URL = "https://www.fubon.com/banking/personal/deposit/exchange_rate/exchange_rate_tw.htm"
URL_2 = "https://ebank.taipeifubon.com.tw/B2C/cfhqu/cfhqu009/CFHQU009_Home.faces?menuId=CFH02011&"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(URL_2, headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")
# print(soup)
currency = str(soup.table.contents[9].contents[1].contents).split()[1].split(">")[1]
rate = float(soup.table.contents[9].contents[3].contents[0])
# print(currency)
# print(rate)

try:
    if currency == "人民9幣":
        if rate < RATE_TO_SELL:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            to_log = f"Now its a good time to sell your RMB.\n{current_time} - {rate}\n"
            subject_success = "Good RMB Rate Now"
            body_success = f"Now its a good time to sell your RMB.\n{current_time} - {rate}"
            em = EmailMessage()
            em['From'] = APP_ADMIN_EMAIL
            em['To'] = recipient
            em['Subject'] = subject_success
            em.set_content(body_success)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as connection:
                connection.login(APP_ADMIN_EMAIL, GMAIL_SECRET_KEY)
                connection.sendmail(APP_ADMIN_EMAIL, recipient, em.as_string())
            print(f"Email sent to Audrey!")

            # with smtplib.SMTP("smtp.exmail.qq.com") as connection:
            #     connection.starttls()
            #     connection.login(MY_EMAIL, PASSWORD)
            #     connection.sendmail(from_addr=MY_EMAIL, to_addrs=APP_ADMIN_EMAIL,
            #                         msg=f"Subject:Good RMB Rate Now\n\nNow its a good time to sell your RMB.\n{current_time} - {rate}")

            with open("rate_log.txt", mode="w") as file:
                file.writelines(to_log)
                print("log_updated")
    else:
        subject_failed = "Update your app."
        body_failed = f"There are some changes in Fubon exchange rate page! Update your soup."
        em = EmailMessage()
        em['From'] = APP_ADMIN_EMAIL
        em['To'] = APP_ADMIN_EMAIL2
        em['Subject'] = subject_failed
        em.set_content(body_failed)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
            connection.login(APP_ADMIN_EMAIL, GMAIL_SECRET_KEY)
            connection.sendmail(APP_ADMIN_EMAIL, APP_ADMIN_EMAIL2, em.as_string())

        # with smtplib.SMTP("smtp.exmail.qq.com") as connection:
        #     connection.starttls()
        #     connection.login(MY_EMAIL, PASSWORD)
        #     connection.sendmail(from_addr=MY_EMAIL, to_addrs=APP_ADMIN_EMAIL,
        #                         msg=f"Subject:Update your app.\n\nThere are some changes in Fubon exchange rate page! Update your soup.")
        print("There are some changes in Fubon exchange rate page! Update your soup.")
except:
    subject_error = "Check your app."
    body_error = f"There are some errors in your program, debug required."
    em = EmailMessage()
    em['From'] = APP_ADMIN_EMAIL
    em['To'] = APP_ADMIN_EMAIL2
    em['Subject'] = subject_error
    em.set_content(body_error)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
        connection.login(APP_ADMIN_EMAIL, GMAIL_SECRET_KEY)
        connection.sendmail(APP_ADMIN_EMAIL, APP_ADMIN_EMAIL2, em.as_string())

    # with smtplib.SMTP("smtp.exmail.qq.com") as connection:
    #     connection.starttls()
    #     connection.login(MY_EMAIL, PASSWORD)
    #     connection.sendmail(from_addr=MY_EMAIL, to_addrs=APP_ADMIN_EMAIL,
    #                         msg=f"Subject:Check your app.\n\nThere are some error in the program, debug required.")
    print("There are some error in the program, debug required.")
else:
    print("Process finished!")