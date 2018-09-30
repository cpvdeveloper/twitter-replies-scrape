import twitter
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from secrets import consumer_key, consumer_secret, access_token_key, access_token_secret

# api credentials
api = twitter.Api(consumer_key = consumer_key,
                    consumer_secret = consumer_secret,
                    access_token_key = access_token_key,
                    access_token_secret = access_token_secret)

# global variable to store all replies
all_replies = []

def find_tweet_ids(name, iterations):
    """
    :param name: twitter username set as the screen_name argument, string
    :param iterations: number of batches of tweets to return, integer
    :return: a set of unique tweet ids
    """

    global api

    # store the ids of tweets that will later by scraped for replies
    tweet_ids = []

    # 
    max_id = ''
    for i in range(iterations):
        statuses = api.GetUserTimeline(screen_name='districtline', exclude_replies=True, count=200, max_id=max_id)
        for idx in range(len(statuses)):
            tweet_ids.append(str(statuses[idx].id))
        max_id = min(tweet_ids)
    return set(tweet_ids)

def find_replies(tweet_id, name):
    """
    Finds all the replies left on the specified tweets
    :param tweet_id: id of the tweet being scraped for replies, integer
    :param name: twitter username, string
    :return: array of all replies
    """
    
    global all_replies

    r = requests.get("https://twitter.com/" + name + "/status/" + str(tweet_id))
    assert r.status_code == 200
    content = r.content
    html_soup = bs(content, "html.parser")
    replies = html_soup.find_all("p", {"class": "TweetTextSize js-tweet-text tweet-text"})
    for reply in replies:
        all_replies.append(reply.text)
    return all_replies

def generate_stopwords():
    """
    Stopwords will not be included in the wordcloud
    :return: a list inclluding standard and custom stopwords
    """

    # a standard list of common stopwords 
    stopwords = set(STOPWORDS)

    # custom stopwords that we don't want
    stopwords_custom = ["aria", "img", "Emoji", "atreply", "twitter", "Hi", "train", "district", "service"]

    # TODO - station names are to be expected but aren't very interesting
    station_names = []

    for word in stopwords_custom:
        stopwords.add(word)
    return stopwords

def show_wordcloud(fnc_stopwords, dataframe, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=fnc_stopwords(),
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

def main():

    name, iterations = input("Enter a target twitter handle and number of iterations, separated by a space: \n").split(' ')

    tweet_ids = find_tweet_ids(name, int(iterations))
    print("Found {} tweet ids".format(len(tweet_ids)))

    if tweet_ids:
        for id in tweet_ids:
            find_replies(id, name)

        df = pd.DataFrame(all_replies)
        print(df)
        show_wordcloud(generate_stopwords, df)

if __name__ == '__main__':
    try:
        api.VerifyCredentials()
        main()
    except Exception as err:
        print(err)
