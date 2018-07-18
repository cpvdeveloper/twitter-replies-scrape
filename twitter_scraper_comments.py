import twitter
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

api = twitter.Api(consumer_key='your_consumer_key',
                    consumer_secret='your_consumer_secret',
                    access_token_key='your_access_token_key',
                    access_token_secret='your_access_token_secret')

all_comments = []

def find_tweet_ids(name):
    """
    :param name: twitter username, string
    """
    statuses = api.GetUserTimeline(screen_name=name, exclude_replies=True, count=20)
    tweet_ids = []
    for idx, val in enumerate(statuses):
        tweet_ids.append(str(statuses[idx].id))
    return tweet_ids

def find_comments(tweet_id):
    """
    :param tweet_id: string
    """
    content = requests.get("https://twitter.com/" + name + "/status/" + str(tweet_id)).content
    html_soup = bs(content, "html.parser")
    comments = html_soup.find_all("p", {"class": "TweetTextSize js-tweet-text tweet-text"})
    for comment in comments:
        all_comments.append(comment.text)
    return all_comments

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df

def main(name):
    try:
        api.VerifyCredentials()
    except Exception as err:
        print(err.message)

    find_tweet_ids(name)
    for id in tweet_ids:
        find_comments(id, name)
    create_dataframe(all_comments)
    print(df)

main('districtline')
