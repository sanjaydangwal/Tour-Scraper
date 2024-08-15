import os
import smtplib
import sqlite3
import ssl
import time

import requests
import selectorlib
from dotenv import load_dotenv

load_dotenv()

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}


connection = sqlite3.connect("data.db")


def scrape(url, headers):
    """Scrape the page source from URL."""
    response = requests.get(url, headers=headers)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    sender = os.getenv("SENDER")
    password = os.getenv("PASSWORD")
    receiver = os.getenv("RECEIVER")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

    print("email sent.")


def store_tour(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    # band, city, date = row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read_tours(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?", (band, city, date))
    rows = cursor.fetchall()
    # cursor.close()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL, HEADERS)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read_tours(extracted)
            if not row:
                send_email("Hey, New event was found!")
                store_tour(extracted)
        time.sleep(2)
