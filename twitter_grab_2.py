import tweepy
#import string #used in washing_machine()
import json #This library is necessary for dumping to a json file
from twitt_auth import *
from pprint import pprint #pretty-print dictionaries or json.  Useful for testing
#import HTMLParser #used in washing_machine()
#from nltk.corpus import stopwords #used in washing_machine()
from washing_machine_2 import * #This is the function which cleans the tweet text
#import re #used in washing_machine()
#from nltk.stem.snowball import SnowballStemmer #used in washing_machine()

print consumer_key


#---------------------------------------------------------------------------------

# Twitter O-Auth credentials and information grab

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())




# Define API search parameters.  I can also use different functions in tweepy to grab a certain user's timeline, or many other info-grab methods.  This is just one of many types of information I can grab.

tweetlist = api.search(q="windows 10", count=1, lang="en")

#---------------------------------------------------------------------------------


# These two lines dump the return of the O-Auth call to a .txt or .json file
# I want to dump to a DB isntead, but this could be useful for testing.

with open("out_raw_tweets.json", "w") as outfile:
       json.dump(tweetlist, outfile, sort_keys=True, indent=4)




#Each item in this list is all of the information associated with one tweet.
#The items in this list are type dictionary.

list_o_dicts = []

# This loop will create a list of dictionaries.  Each dictionary, i.e. each element in the list, is the information from one tweet.



############################
#write in a clause to say, "if this item doesnt exist, write None or Null for the value
#This is what the .get() method does.  If the key doesnt exist, it writes the value as None
############################




##################
#When dumping this data to my postgresql database, need to search DB for a unique identifier, and if that identifier exists in the DB then don't write the current object.
# This is necessary to avoid duplicates, which could really screw up statistical calculations if something is duplicated over and over

# Retweets need to be considered when analysing the date, because if a status is retweeted 1000 times, itll throw my shit off.

# Or maybe I just want to store data that is not a retweet?
## ??????????????????????????????????????????????????











info = {}

for i in range(len(tweetlist["statuses"])):
	info["query"] = tweetlist["search_metadata"].get("query", None)
	info["status_contributors"] = tweetlist["statuses"][i].get("contributors", None)
	info["status_coordinates"] = tweetlist["statuses"][i].get("coordinates", None)
	info["status_created_at"] = tweetlist["statuses"][i].get("created_at", None)

	hashtags = []
	for j in range(0, len(tweetlist["statuses"][i]["entities"]["hashtags"])):
		hashtags.append(tweetlist["statuses"][i]["entities"]["hashtags"][j].get("text", None))
	if hashtags:  #This conditional says, if the list is empty force it to None instead of []
		info["status_hashtags"] = hashtags
	else:
		info["status_hashtags"] = None

	user_mentions = []
	for j in range(0, len(tweetlist["statuses"][i]["entities"]["user_mentions"])):
	        user_mentions.append(tweetlist["statuses"][i]["entities"]["user_mentions"][j].get("screen_name", None))
	if user_mentions: #This conditional says, if the list is empty force it to None instead of []
		info["status_user_mentions"] = user_mentions
	else:
		info["status_user_mentions"] = None

	info["status_favorite_count"] = tweetlist["statuses"][i].get("favorite_count", None)
	info["status_id"] = tweetlist["statuses"][i].get("id", None)
	info["status_in_reply_to_screen_name"] = tweetlist["statuses"][i].get("in_reply_to_screen_name", None)
	info["status_in_reply_to_status_id"] = tweetlist["statuses"][i].get("in_reply_to_status_id", None)
	info["status_in_reply_to_user_id"] = tweetlist["statuses"][i].get("in_reply_to_user_id", None)
	info["status_is_quote_status"] = tweetlist["statuses"][i].get("is_quote_status", None)
	info["status_lang"] = tweetlist["statuses"][i].get("lang", None)
	info["status_metadata_iso_lang_code"] = tweetlist["statuses"][i]["metadata"].get("iso_language_code", None)
	info["status_metadata_result_type"] = tweetlist["statuses"][i]["metadata"].get("result_type", None)
	info["status_place"] = tweetlist["statuses"][i].get("place", None)
	info["status_retweet_count"] = tweetlist["statuses"][i].get("retweet_count", None)
	info["status_text"] = tweetlist["statuses"][i].get("text", None)
	info["status_text_clean"] = washing_machine(tweetlist["statuses"][i].get("text", " "), expansions)
	info["user_created_at"] = tweetlist["statuses"][i]["user"].get("created_at", None)
	info["user_description"] = tweetlist["statuses"][i]["user"].get("description", None)
#	info["user_entities"] = tweetlist["statuses"][i]["user"].get("entities", None)
	info["user_friends_count"] = tweetlist["statuses"][i]["user"].get("friends_count", None)
	info["user_id"] = tweetlist["statuses"][i]["user"].get("id", None)
	info["user_lang"] = tweetlist["statuses"][i]["user"].get("lang", None)
	info["user_listed_count"] = tweetlist["statuses"][i]["user"].get("listed_count", None)
	info["user_location"] = tweetlist["statuses"][i]["user"].get("location", None)
	info["user_name"] = tweetlist["statuses"][i]["user"].get("name", None)
	info["user_screen_name"] = tweetlist["statuses"][i]["user"].get("screen_name", None)
	info["user_statuses_count"] = tweetlist["statuses"][i]["user"].get("statuses_count", None)
	info["user_time_zone"] = tweetlist["statuses"][i]["user"].get("time_zone", None)
	info["user_url"] = tweetlist["statuses"][i]["user"].get("url", None)
	info["user_utc_offset"] = tweetlist["statuses"][i]["user"].get("utc_offset", None)
	info["user_verified"] = tweetlist["statuses"][i]["user"].get("verified", None)

# maybe as I go through and grab all the info I want from each status I should delete that status from tweetlist to conserve memory?
	list_o_dicts.append(info)
	info = {}
#test to see if i get encoding errors with the following:
	


with open("out__1.json", "w") as outfile:
       json.dump(list_o_dicts, outfile, sort_keys=True, indent=4)


del tweetlist
del list_o_dicts

