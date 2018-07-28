import twitter
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

api = twitter.Api(consumer_key='your_consumer_key',
                    consumer_secret='your_consumer_secret',
                    access_token_key='your_token_key',
                    access_token_secret='your_token_secret')

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
        for idx in range(len(statuses)):
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

def stopwords():
    stopwords = set(STOPWORDS)
    stopwords_custom = ["aria", "img", "Emoji", "atreply", "twitter", "Hi", "train", "district", "service"]
    station_names = []
    for word in stopwords_custom:
        stopwords.add(word)
    return stopwords

def show_wordcloud(dataframe, stopwords, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=100,
        max_font_size=60, 
        scale=5,
        #random_state=1
    ).generate(str(dataframe))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

def main(name, iterations):
    try:
        api.VerifyCredentials()
    except Exception as err:
        print(err.message)

    tweet_ids = find_tweet_ids(name, iterations)
    print(tweet_ids)
    for id in tweet_ids:
        find_comments(id, name)
    df = pd.DataFrame(all_comments)
    show_wordcloud(df, stopwords)

main('districtline', 1)
