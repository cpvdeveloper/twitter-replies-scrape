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

def find_tweet_ids(name, iterations):
    """
    :param name: twitter username, string
    :param iterations: integer
    :return: a set of unique tweet ids
    """
    tweet_ids = []
    max_id = ''
    for i in range(iterations):
        statuses = api.GetUserTimeline(screen_name=name, exclude_replies=True, count=200, max_id=max_id)
        for idx, val in enumerate(statuses):
            tweet_ids.append(str(statuses[idx].id))
        max_id = min(tweet_ids)
    return set(tweet_ids)

def find_comments(tweet_id, name):
    """
    Finds all the comments left on the specified tweets
    :param tweet_id: integer
    :param name: string
    :return: array of all comments
    """
    content = requests.get("https://twitter.com/" + name + "/status/" + str(tweet_id)).content
    html_soup = bs(content, "html.parser")
    comments = html_soup.find_all("p", {"class": "TweetTextSize js-tweet-text tweet-text"})
    for comment in comments:
        all_comments.append(comment.text)
    return all_comments

def create_dataframe(data):
    """
    Converts an array of into dataframe
    :param data:
    :return: dataframe
    """
    df = pd.DataFrame(data)
    return df

def main(name, iterations):
    try:
        api.VerifyCredentials()
    except Exception as err:
        print(err.message)

    tweet_ids = find_tweet_ids(name, iterations)
    print(tweet_ids)
    for id in tweet_ids:
        find_comments(id, name)
    df = create_dataframe(all_comments)
    print(df)

main('districtline')
