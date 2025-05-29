import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import os
import datetime
import snowflake.connector
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
conn = snowflake.connector.connect(user = os.environ.get('SNOWFLAKE_USER'),
                                    password = os.environ.get('SNOWFLAKE_PASSWORD'),
                                    account = os.environ.get('SNOWFLAKE_ACCOUNT'),
                                    warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE'),
                                    database = os.environ.get('SNOWFLAKE_DATABASE'),
                                    schema = os.environ.get('SNOWFLAKE_SCHEMA')


)
cursor = conn.cursor()
insert_query = """
INSERT INTO sentiment_data (
    date, textblob_polarity, vader_neg, vader_neu, vader_pos, vader_compound,
    positive_mentions, negative_mentions
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.execute(insert_query, (
    date_now,
    polarity,
    vander_scores['neg'],
    vander_scores['neu'],
    vander_scores['pos'],
    vander_scores['compound'],
    positive_counter,
    negative_counter
))

conn.commit()
cursor.close()
conn.close()





