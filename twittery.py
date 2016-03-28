#!/usr/bin/env python

import tweepy
import scrollphat
from time import sleep
import config

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"


def print_tweet(tweet):
    scrollphat.clear()
    scrollphat.set_brightness(7)
    scrollphat.write_string(tweet)
    x = 0
    # scroll the message twice
    while x < (scrollphat.buffer_len()*2):
        scrollphat.scroll()
        sleep(0.1)
        x += 1
    scrollphat.clear()

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweet_list = []

    while True:
        tweets = api.mentions_timeline()[0:2]  # no way I'll have more than 2 new ones :D
        for tweet in tweets:
            if tweet.id not in tweet_list:
                # get text to scroll and turn to uppercase for easy reading
                tweet_to_print = '--> %s TWEETED: %s ' % (tweet.user.name.upper(), tweet.text.upper())
                # ignore non ascii characters like emojis as scrollphat cannot display them
                tweet_to_print = tweet_to_print.encode('ascii', 'ignore').decode('ascii')
                print_tweet(tweet_to_print)
                tweet_list.append(tweet.id)
                if len(tweet_list) > 5:
                    # make sure tweet list won't get too big
                    tweet_list.pop(0)
        sleep(120) # avoid hitting rate limit
