# -*- coding: utf-8 -*-
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy
import pandas as pd
from pandas.io.json import json_normalize

def is_name_in_it(target, ns_eng, ns_loc):
    ns_eng_norm = ns_neg.lower().replace(" ", "")
    ns_loc_norm = ns_loc.lower().replace(" ", "")
    target_norm = ns_loc.lower().replace(" ", "")
    return (ns_eng_norm in target_norm or ns_loc_norm in target_norm)

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

# output (twitter ids)
df = pd.DataFrame(columns=['country',
                           'national society (english)',
                           'national society (local language)',
                           'red cross name (local language)',
                           'id',
                           'name',
                           'screen name',
                           'location'])

# input (names of national societies)
#df_names = pd.read_csv('contacts_clean.csv')
#national_societies = df_names['name'].values
df_info = pd.read_excel('../pilot_countries_metadata.xlsx', index_col=0)
national_societies_eng = df_info['name (english)'].values
national_societies_loc = df_info['name (local language)'].values
countries = df_info['country'].values
redcross_name_loc = df_info['red cross name (local language)'].values

for country, ns_eng, ns_loc, rc_name_loc in zip(countries,
                                                national_societies_eng,
                                                national_societies_loc,
                                                redcross_name_loc):
    
    users = api.search_users(ns_eng)
    
    for user in users:
        user_data = user._json
        df = df.append({'country': country,
                        'national society (english)': ns_eng,
                        'national society (local language)': ns_loc,
                        'red cross name (local language)': rc_name_loc,
                        'id': user_data['id'],
                        'name': user_data['name'],
                        'screen name': user_data['screen_name'],
                        'location': user_data['location'],}, ignore_index=True)
    
    users = api.search_users(ns_loc)
    
    for user in users:
        user_data = user._json
        df = df.append({'country': country,
                        'national society (english)': ns_eng,
                        'national society (local language)': ns_loc,
                        'red cross name (local language)': rc_name_loc,
                        'id': user_data['id'],
                        'name': user_data['name'],
                        'screen name': user_data['screen_name'],
                        'location': user_data['location'],}, ignore_index=True)
# drop duplicates
df = df.drop_duplicates()

# remove accounts which do not have "red cross" in their name
def is_name_in_it(row):
    ns_eng_norm = row['red cross name (local language)'].lower().replace(" ", "")
    ns_loc_norm = str("Red Cross").lower().replace(" ", "")
    target_norm = row['name'].lower().replace(" ", "")
    return ((ns_eng_norm in target_norm or ns_loc_norm in target_norm) and
            ("ifrc" not in target_norm and "icrc" not in target_norm))

df['is_good'] = df.apply(is_name_in_it, axis=1)
df = df[df['is_good']].drop(columns=['is_good'])

# print and save to file
print(df.head())
df.to_csv('pilot_countries_twitter_ids.csv', sep='|')
                       
                       
                       
                       
                       
