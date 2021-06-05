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
import threading
from time import sleep
import keyboard


elon_id = '44196397'
trump_id = '25073877'
api_key = '6RBmryKPu85afiw2tEAkB5tdX'
api_secret_key = 'HFxObpxXdesgh2Ek9XX7CHGiL9jDmoQ1ELuzAz6XscGQaVRBDp'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALgPIgEAAAAACDtHiYpojF3KP%2BHyBfnNpXXy4lI%3DNDPkSsetDQskwK5jlG2n4sPurTaffrbID4VoehI0cKun7bx13g'

#use api_username and password (key and secret) to obtain user access token
callback_uri = 'oob'
auth = tweepy.OAuthHandler(api_key, api_secret_key, callback_uri)
redirect_url = auth.get_authorization_url()
print(redirect_url)
webbrowser.open(redirect_url)
#changes for each user to obtain the access tokens
user_code = input('What\'s the code? ')
auth.get_access_token(user_code)
api = tweepy.API(auth)
print(auth.access_token, auth.access_token_secret)


#print(elon)
#print(me)
trump = api.get_user(trump_id)
#print(trump)

elon_tweets = api.search('@elonmusk')
elon_tweets
#elon_tweets_text = elon_tweets[i['description'] for i in elon_tweets]
#print(dir(elon_tweets))
#print(dir(me))
#print(type(vars(elon_tweets)))

elon_timeline = api.user_timeline('@elonmusk', count = 25)

def timeline_to_db(timeline):
    columns = set()
    timeline_data = []
    allowed = [str, int]
    for i in timeline:
        single_status = {'user': i.user.screen_name}

        status_dict = dict(vars(i))
        status_keys = status_dict.keys()
        for j in status_keys:
            key_type = type(status_dict[j])
            if key_type != None:
                if key_type in allowed:
                    single_status[j] = status_dict[j]
                    columns.add(j)
        timeline_data.append(single_status)
    columns.add('user')
    head_cols = list(columns)
    df = pd.DataFrame(timeline_data, columns = head_cols)
    return df

elon_timeline_db = timeline_to_db(elon_timeline)
elon_timeline_db.head()

trump_timeline = api.user_timeline('realDonaldTrump', count=25)
df = timeline_to_db(trump_timeline)
df.head()

#elon counter data for function

elon_text1 = []
elonmusk = 'elonmusk'
for i, status in enumerate(tweepy.Cursor(api.user_timeline, screen_name = elonmusk).items(50)):
    elon_text1.append(status.text)
pre_elon_text = []
for j in elon_text1:
    elon_tweet = j.split(' ')
    
    pre_elon_text.append(elon_tweet)
elon_text_final = []
for z in pre_elon_text:
    for y in z:
        elon_text_final.append(y)
    
#print(Counter(elon_text_final))
elon_counter = Counter(elon_text_final)

#elon function

elon_words = 0
for i in elon_counter:
    elon_words += elon_counter[i]

def how_elon(statement):
    elon_score = 0
    statement_words = statement.split(' ')
    for i in statement_words:
        elon_score += elon_counter[i]
    result = f'You\'re score is {elon_score}... You can be more like Elon.'
    return result
how_elon('The school system is wrong')

#version one time_predictor (elon):

hour_of_tweet = []
for i in elon_timeline:
    s = str(i.created_at).split(' ')
    time_of_day = s[1].split(':')
    hour_of_day = time_of_day[0]
    hour_of_tweet.append(hour_of_day)

        
    
print(hour_of_tweet)
meal_labels = []
for i in hour_of_tweet:
    if int(i) < 12 and int(i) >= 5:
        meal_labels.append(0)
    elif int(i) >= 12 and int(i) < 22:
        meal_labels.append(1)
    else: 
        meal_labels.append(2)
print(meal_labels)

elon_tweet_list = []
for i in elon_timeline:
    elon_tweet_list.append(i.text)

training_data, testing_data, training_labels, testing_labels = train_test_split(elon_tweet_list, meal_labels, random_state = 1, test_size = 0.2)
counter = CountVectorizer()
counter.fit(training_data)
training_counts = counter.transform(training_data)
testing_counts = counter.transform(testing_data)
classifier = MultinomialNB()
classifier.fit(training_counts, training_labels)
predictions = classifier.predict(testing_counts)
my_tweet = 'sleep is great'
my_count = counter.transform([my_tweet])
my_tweet_prediction_time = classifier.predict(my_count)
print(predictions)
print(my_tweet_prediction_time)
print(accuracy_score(testing_labels, predictions))
print(elon_tweet_list)
print(len(training_data))

evt = threading.Event()
result = None
def background_task(): 
    global result
    print("start")
    result = "Started"
    sleep(5)
    print("stop")
    result = "Finished"
    evt.set()
t = threading.Thread(target=background_task)
t.start()
#optional timeout
timeout=1
evt.wait(timeout=timeout)
print(result)

def p():
    while True:
        sleep(2)
        if keyboard.is_pressed("p"):
                print("You pressed p")
                break

