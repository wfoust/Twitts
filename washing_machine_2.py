#This is the file that houses the function that cleans text.
#This function will be passed one individual tweet.  i.e. one string
#since this function will be called many times from the parent function, make sure apostrophe dictionary is passed to function and that all necessary libraries are called in main program prior to this function call.

import HTMLParser
from nltk.corpus import stopwords
import re
import string
import codecs
from nltk.stem.snowball import SnowballStemmer
#######################################################################



# This creates a dictionary of contractions from a separate file.  This is necessary for a certain stage in the funtion washing_machine().
expansions = {}
with open("expansions.txt", "r") as f:
        for line in f:
                linelist = line.rstrip('\n').split(',')
                expansions[linelist[0]] = linelist[1]








def washing_machine(tweet, appdictionary): # tweet = string

#def washing_machine(tweet): # tweet = string



##  1  #####################################################################
##  Escape HTML characters.  I.E. turn ' &lt;3' into '<3'
	tweet = HTMLParser.HTMLParser().unescape(tweet)


##  2  #####################################################################
##  Remove URLs from tweet text
	tweet = re.sub(r'(https?://[^\s]+)', '', tweet)


##  3  #####################################################################
##  Remove punctuation
#this method kind of looks ugly, but turns out it's really efficient

#ideally, I should build 'table' and pass it to the function, just like the dictionary in step 3.

	punctuation = u'!"$%&()*+,-./:;?[\\]^_`{|}~#'
#	print("Type: ", type(tweet))
#	punctuation = '!"$%&()*+,-./:;?[\\]^_`{|}~#'
	table = dict((ord(char), None) for char in punctuation)
	tweet = tweet.translate(table)

#Removal of punctuation is set up this way because I'm passing it a unicode string.  If I am passing it a 'normal' string (type='str'), I would instead use:

#	punctuation = '!"$%&()*+,-./:;?[\\]^_`{|}~'
#	to = '                          '
#	table = string.maketrans(punctuation, to)
#	tweet = tweet.translate(table)





## 4 #######################################################################
##  Remove all non-ascii characters:

	tweet = filter(lambda x: ord(x)<128, tweet)


##  5  #####################################################################
##  Decode data
	tweet = tweet.encode('ascii', 'ignore')


##  6  #####################################################################
##  Apostrophe lookup
	for word in tweet.split():
	        if word in appdictionary:
         	       tweet = tweet.replace(word, appdictionary[word])	



##  7  #####################################################################
##  Split attached words
#	tweet = re.sub(r"(\w)([A-Z])", r"\1 \2", tweet)
#This is causing problems if a person types in all caps, which is common


##  8  #####################################################################
##  Force all text to lower case
	tweet = tweet.lower()



##  9  #####################################################################
##  Remove stop words
	tweet = [i for i in tweet.split() if i not in stopwords.words('english')] #this returns a list of strings (each word is an item in the list)
	tweet = " ".join(tweet) #this turns that list back into a string






##  10  #####################################################################
##  Stem text
#I think I'll use the snowball stemmer.  Lots of choices of stemming algorithms

#should assign following line only once if possible
#	stemmer = SnowballStemmer("english")
#	stemmed_tweet = ""
#	for word in tweet.split():
#		stemmed_tweet += str(stemmer.stem(word)+" ")


#	return(stemmed_tweet)
	return(tweet)






#text = "This is my tweet, TheseWordsareAttached.  #FeelTheBern rabble rabble &lt;3 does this work? Isn't this https://feelthebern.org great?  It should work, shouldn't it?  http://www.google.com"

#expansions = {}
#with open("expansions.txt", "r") as f:
#        for line in f:
#                linelist = line.rstrip('\n').split(',')
#                expansions[linelist[0]] = linelist[1]
# expansions is a dictionary of contractions



