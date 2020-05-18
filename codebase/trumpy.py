#!/usr/bin/python3

"""File that downloads tweets and analyze them."""

__author__="J Jacob Wikner, jjwikner@gmail.com"
__copyright__="None"

import os
import tweepy as tw
import pandas as pd
import argparse

class trumpy():
    
    def __init__(self, keyfile="/home/jjwikner/keys/twitter_keys.txt"):
        """Init function"""

        self.keys = dict()
        self.read_keys(keyfile)
        self.connect_api()


    def connect_api(self):

        auth = tw.OAuthHandler(self.keys["consumer_key"], 
                               self.keys["consumer_secret"])
        auth.set_access_token(self.keys["access_token"], 
                              self.keys["access_token_secret"])
        self.api = tw.API(auth, 
                          wait_on_rate_limit=True)
        


    def read_keys(self, keyfile="/home/jjwikner/keys/twitter_keys.txt"):
        
        with open(keyfile,'r') as file:
            keys = file.readlines()

        for key in keys:
            key_sub_dict = key.strip().split("=",1)
            self.keys[key_sub_dict[0]] = key_sub_dict[1]



    def search_tweets(self, search_token="#liu", no_tweets=5, start_date="2018-01-01"):
        """Search tweets for words/hash tags, etc."""
        tweets = tw.Cursor(self.api.search,
                           q=search_token,
                           lang="en",
                           since=start_date).items(no_tweets)

        for tweet in tweets:
            print(tweet.text)

    def get_tweets(self, user="@realDonaldTrump", no_tweets=11, include_retweets=False):
        """Get the tweets from a specific user. The data is returned as a csv-type file."""
        tweets = self.api.user_timeline(screen_name=user, 
                                        count=no_tweets, 
                                        tweet_mode='extended')
        tweets_as_csv = [tweet.full_text for tweet in tweets]
        all_tweets=[]

        for tweet in tweets_as_csv:

            if include_retweets:
                all_tweets.append(tweet)
            else:
                if not( tweet[0:3] == "RT " ):
                    # Do not include retweets
                    all_tweets.append(tweet)
                    
        return all_tweets
        
    def update(self, message="This message is intentionally left blank."):
        """ Performs a status update. """
        self.api.update_status(message)

    
    def self_test(self):
        """A self_test function for some test functionalities."""
        print("Example of hashtag search. =============")
        self.search_tweets()
        print("Example of user search. =============")
        for (no, tweet) in enumerate(self.get_tweets()):
            print(f"{1+no} : {tweet}")
            

# === 

def main(the_options):
    tweng = trumpy()

    if the_options.test:
        tweng.self_test()
    
    if the_options.user is not None:
        for (no, tweet) in enumerate(tweng.get_tweets(user=the_options.user, no_tweets=the_options.no)):
            print(f"{1+no} : {tweet}")

    print(the_options.no)
    # tweng.update()
        
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Harvest among the tweets.')
    parser.add_argument('--verbose',
                        help='Print or not',
                        action='store_true')

    parser.add_argument('--user', help="User to harvest from.", default=None)
    parser.add_argument('--test', help="Run the tests.", action="store_true")
    parser.add_argument('--no', help="Number of tweets.", type=int, default=10)


    args = parser.parse_args()
    main(args)
