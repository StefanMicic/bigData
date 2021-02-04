#!/usr/bin/python3

import os
import time

import kafka.errors
import requests
from bs4 import BeautifulSoup
from kafka import KafkaProducer

SUBREDDIT = os.environ["SUBREDDIT"]
KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "subreddit-" + SUBREDDIT

while True:
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER.split(","))
        print("Connected to Kafka!")
        break
    except kafka.errors.NoBrokersAvailable as e:
        print(e)
        time.sleep(3)


url = "https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv"
r = requests.get(url=url)
# Create a BeautifulSoup object
soup = BeautifulSoup(r.text, "html.parser")
movies = list()
for movie in soup.find_all("a", href=True):
    if "/title/" not in movie["href"]:
        continue
    movies.append("https://www.imdb.com" + movie["href"])

for link in movies[1::2]:
    text = requests.get(url=link)
    soup = BeautifulSoup(text.text, "html.parser")
    summary_text = soup.find("div", {"class": "summary_text"})
    # data["summary_text"] = summary_text.string.strip()
    print(summary_text.string.strip())
    print("SALJEM scrape")
    producer.send(
        TOPIC,
        key=bytes(summary_text.string.strip(), "utf-8"),
        value=bytes(summary_text.string.strip(), "utf-8"),
    )
