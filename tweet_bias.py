import time
import tweepy
import webbrowser
import asyncio
import sklearn
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import lxml
from bs4 import BeautifulSoup as bs
import requests
import threading
import keyboard
from time import sleep

#alr we r here to make a prediction algorithm that posesses intuitive knowledge on the when aspect
# of a future tweet with maximum accuracy

#what information will show a pattern of when a tweet is posted?:
#{news: obtain information from news sources on the internet?, 
# personal whim/personal reasons: more ambiguous part of the intuitive aspect, 
# }

#use lxml parser with beautiful soup and get requests to get information from websites?

#how to constantly be aware of new news?

#web scraping and parse testing with bs4:



#Version 1: while loop that activates as soon as a headline changes 
# (st like while headline == x: don't activate ML algorithm
# new idea: use threading additionally... have the while loop run as a thread
# and thread.join() as soon as the while loop terminates
# activating the next thread aka the XxTrumpxX ML algorithm)

# The algorithm: training data as only news for now with (Dilemna... the new algorithm
# isn't accurately described as predicting when a tweet will be posted, since the news
# will either result in a tweet or not. it will specifically predict if a tweet will be posted
# after a news source changes info, taking in that data and performing sentiment analysis
# on if and with what influence the tweet will have)

# but how... the data in a news source needs to be compared with previous data 
# that has been fitted to the ML algorithm. this is supervised ML so i will have to label 
# each group of text on whether it's, for example, democrat or republican favoring, 
# which results in two classes. for version one, a counter object for each articles text 
# will be created, and the score of the new news will either be 0 or 1 based on 
# a probability of its content being either dem or rep favoring

#data and party labels

CNN = requests.get('https://www.cnn.com', 'lxml')
CNN_text = CNN.text
CNN_soup = bs(CNN_text, 'lxml')


#print(article1_soup.text)
def soupifier(url):
    article = requests.get(url)
    article_text = article.text
    article_soup = bs(article_text, 'lxml')
    name = []
    name.append(article_soup.text)
    return name
darticle1 = soupifier('https://www.cnn.com/2020/10/16/politics/barrett-questionnaire-supplemented-kfile/index.html')
darticle2 = soupifier('https://www.cnn.com/2020/10/16/politics/barrett-questionnaire-supplemented-kfile/index.html')
darticle3 = soupifier('https://www.cnn.com/2020/10/16/politics/joe-biden-trump-whitmer-kidnapping-plot/index.html')

dem_articles = [darticle1[0], darticle2[0], darticle3[0]]

rarticle2 = soupifier('https://www.foxnews.com/politics/pelosi-trump-talks-person-to-person')
rarticle1 = soupifier('https://www.foxnews.com/politics/twitter-employees-openly-rip-trump-praise-biden-trump-must-be-defeated')
rarticle3 = soupifier('https://www.foxnews.com/politics/trump-rips-ben-sasse-nebraska-senators-diatribe-against-president')

rep_articles = [rarticle1[0], rarticle2[0], rarticle3[0]]

labels = [0] * len(dem_articles) + [1] * len(rep_articles)
#print(labels)

articles = []
for i in dem_articles:
    articles.append(i)
for i in rep_articles:
    articles.append(i)
#print(articles)
training_data, testing_data, training_labels, testing_labels = train_test_split(articles, labels, test_size=0.2, random_state=0)

counter = CountVectorizer()
counter.fit(training_data)
training_counts = counter.transform(training_data)
testing_counts = counter.transform(testing_data)
classifier = MultinomialNB()
classifier.fit(training_counts,training_labels)
predictions = classifier.predict(testing_counts)
#print(accuracy_score(testing_labels, predictions))
#print(predictions)
#print(testing_labels)

#now that data for determining party bias of an article is complete, 
# apply to any new article that pops up on a specific news source 
# at the instance it does using threads and perhaps while loops

while True:
    site = requests.get('https://cnn.com')
    article_to_read = site.text
    print('loop')
    sleep(5)
    site_changed = requests.get('https://cnn.com')
    article_changed = site_changed.text
    if article_to_read != article_changed:
        print(article_to_read)
        print(article_changed)
        print('changed')
        break

