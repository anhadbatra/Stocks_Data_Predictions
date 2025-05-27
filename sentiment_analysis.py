import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import csv
import datetime
from pyhive import hive
r = requests.get("https://appleinsider.com/")


soup = BeautifulSoup(r.content,'html.parser')
content = ' '.join([p.get_text() for p in soup.find_all('p')])

positive_counter,negative_counter = 0,0
positive_impacts = ['release', 'dominate', 'innovate', 'success', 'improve']
negative_impacts = ['declining', 'failure', 'issue', 'problem', 'delay']
positive_counter = sum(content.lower().count(word) for word in positive_impacts)
negative_counter = sum(content.lower().count(word) for word in negative_impacts)

blob = TextBlob(content)
polarity = round(blob.polarity,5)
analyser = SentimentIntensityAnalyzer()
vander_scores = analyser.polarity_scores(content)
date_now = datetime.date.today()
data = [
    date_now,polarity,vander_scores,positive_counter,negative_counter
]
conn = hive.Connection(
    host='localhost'
    port=10000
    database='stock_prices'
    password=''

)





