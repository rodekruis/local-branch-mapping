# -*- coding: utf-8 -*-
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy
import pandas as pd
import datetime
import logging
logging.basicConfig(filename='twitter_data/get_past_tweets.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
import time

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = 'my-access-token'
ACCESS_SECRET = 'my-access-secret'
CONSUMER_KEY = 'my-consumer-key'
CONSUMER_SECRET = 'my-consumer-secret'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------

# input (accounts of red cross pages)
df_accounts = pd.read_csv('pilot_countries_twitter_ids.csv', index_col=0, sep='|')   
screen_names = df_accounts['screen_name'].values       
     
# get today's date and one week ago      
today = datetime.date.today()
week_ago = today - datetime.timedelta(days=7)

# save output as
save_file = 'twitter_data/tweets_['+today.strftime("%d-%m-%Y")+', '+week_ago.strftime("%d-%m-%Y")+'].json'

# loop over pages, save tweets
for screen_name in screen_names:
    
    try:
        tweets = api.search(q=screen_name, include_entities=True)
        
        for tweet in tweets:
            with open(save_file, 'a') as tf:
                tf.write('\n')
                json.dump(tweet._json, tf)
                
    except tweepy.TweepError as e:
        logging.warning(e.reason, screen_name)
        time.sleep(10)
        pass
        
        
        
                       
                       
                       
                       
                       
