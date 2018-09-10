import tweepy
import markovify
import json

consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

MAX_TIMELINE_POSTS = 200

with open("twitter-credentials.json") as f:
    credentials = json.load(f)

#gets the timeline of a twitter user, 200 tweets at a time, for a choosen number of pages
def get_tweets(n_page, twitter_user_name):

    auth = tweepy.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    auth.set_access_token(credentials["access_key"], credentials["access_secret"])
    api = tweepy.API(auth)

    tweets = []
    for page_number in range(n_page):
        tweets.extend(api.user_timeline(
            screen_name=twitter_user_name,
            count=MAX_TIMELINE_POSTS,
            include_rts=False,
            page=page_number))

    return tweets


#todo: decide if mentions should be included
# removes a bunch of stuff that we don't want to input inside the markov chain
def trim_tweets(tweet):
    processed_text = []

    for word in tweet.text.split(" "):
        if(len(word) > 0 and
           'http' not in word and
           'RT' not in word and
            word[0] != '@' and
           word[0] != '/'):
            processed_text.append(word)
    return " ".join(processed_text)

# prints tweets between 30 and 160 characters using a markov chain
def print_markov_chain_tweet(text, n_tweet):
    markov_model = markovify.text.NewlineText(text)
    for i in range(n_tweet):
        print(markov_model.make_short_sentence(160, 30))


timeline = get_tweets(10, credentials["target_account"]) #get 20 pages of
processed_timeline = [trim_tweets(tweet) for tweet in timeline]
text_timeline = "\n".join(processed_timeline)
#print_markov_chain_tweet(text_timeline, 10)
markov_model = markovify.text.NewlineText(text_timeline)

for i in range(20):
    print(markov_model.make_sentence(tries=10000))
