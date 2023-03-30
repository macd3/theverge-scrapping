#Create a new Python file in VS Code and import the necessary libraries
import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime

#Set the URL of the website to be scraped
url = "https://www.theverge.com/tech"

#Send a GET request to the website and get the HTML content:
response = requests.get(url)
html_content = response.content

#Parse the HTML content using Beautiful Soup:
soup = BeautifulSoup(html_content, "html.parser")

#Find all the articles on the page:
articles = soup.find_all("article")

#Create a CSV file with the header and today's date:
date_today = datetime.date.today().strftime('%d%m%Y')
csv_filename = date_today + '_verge.csv'

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['id', 'URL', 'headline', 'author', 'date'])

#Create an SQLite database and a table to store the scraped data:
conn = sqlite3.connect('verge_articles.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)')

#Loop through each article, extract the relevant information, and save it to the CSV file and SQLite database:
for index, article in enumerate(articles):
    headline = article.find("h2", {"class": "mb-8 font-polysans text-30 font-bold leading-100 sm:text-35"}).text.strip()
    url = article.find("a", {"class": "c-entry-box--compact__image-wrapper"})['href']
    author = article.find("span", {"class": "relative z-10 inline-block pt-4 font-polysans text-11 uppercase leading-140 tracking-15 text-gray-31 dark:text-gray-bd"}).text.strip()
    date = article.find("time")['datetime']

    with open(csv_filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([index+1, url, headline, author, date])

    c.execute('INSERT INTO articles (id, url, headline, author, date) VALUES (?, ?, ?, ?, ?)',
              (index+1, url, headline, author, date))

conn.commit()
conn.close()


