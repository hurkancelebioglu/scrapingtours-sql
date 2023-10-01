import requests
import selectorlib
import os
import ssl
import smtplib

URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "hurkan.celebioglu@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "hurkan.celebioglu@gmail.com"
    my_context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=my_context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent.")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="Hey, new event was found!")
