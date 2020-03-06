import tweepy 
import csv
import numpy as np
import openpyxl as pyxl
import string
import os
import pandas as pnd
import datetime as dt
import re
import time as t
import sys




#Twitter API credentials
consumer_key = "onfYrqpNcYLtPBt02AIYSkQQa"
consumer_secret = "glFPHK6KxF081LFLj1Q9gPomQ5ZhPR7zm6L71SPlBtznDR3u3p"
access_key = "3978353773-JqerLciY42lDBF7wmBwcup4iLxgdviw9ZoEKqP3"
access_secret = "gC1xQ805klowGF8H1ajZAxxUJzy7kLXxbcMQ8KoXWtI4D"

#
def read_TWpagelist():

  print("Reading XL work book")
  df = pnd.read_excel(open('input.xlsx','rb'), sheet_name='Sheet1')
  #df =  df[df.Followers_Count>2000]
  #print((df['scn']))
  return df['TW_Handle']


#
def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,tweet_mode='extended')
    except tweepy.TweepError as twe:
        print('tweepy error')
        print(twe)
        return
    #save most recent tweets
    alltweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    try:
        oldest = alltweets[-1].id - 1
    except IndexError as ex:
        print("User hasn't Tweeted ",ex)
        return
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,tweet_mode='extended')
        
        #print(dir(new_tweets))
        #save most recent tweets
        
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(alltweets[-1].created_at)
        #print(alltweets[-1].full_text)
        print ((len(alltweets)),"... tweets downloaded so far from Handle",screen_name )
    
    #transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text,tweet.retweet_count,tweet.favorite_count,tweet.user.screen_name] for tweet in alltweets]
    print(outtweets[1])
    #df_final=pnd.Series(outtweets)
    #print(df_final)
    write_Xlbook(to_dataframe(alltweets))
    
    return
def to_dataframe(alltweets):
    
    weekday = {'0': 'Monday', '1':'Tuesday' , '2': 'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
    eng_sum=0
    Fk_id=list()
    Name=list()
    Platform=list()
    Post_id=list()
    Link=list()
    Type=list()
    Year=list()
    Day=list()
    Total_engagement=list()
    Like=list()
    Love=list()
    Wow=list()
    Haha=list()
    Angry=list()
    Thankful=list()
    Comment=list()
    Share=list()
    Dislike=list()
    Views=list()
    Genre=list()
    Full_text=list()
    Time=list()
    Time_stamp=list()
    Month=list()

    for tweet in alltweets:

        Fk_id.append('')
        Name.append(tweet.user.screen_name)
        Platform.append("Twitter")
        Post_id.append(str(tweet.id))
        Link.append("https://twitter.com/"+tweet.user.screen_name+"/status/"+str(tweet.id))
        try:
             if 'expanded_url' in str(tweet.entities.get('media')):
                     
                if 'video' in str(tweet.entities.get('media')):
                        Type.append('video')
                else :
                        Type.append('image')
             else :
                   if 'http' in str(tweet.full_text.encode("utf-8")):
                           Type.append('Link')
                   else :
                           Type.append('Text')  
        except AttributeError as e :
                Type.append('Link')
                print("Attribute error is ",e)                    
        #print("Enties are as follows",tweet.entities.get('hashtags'))
        Year.append(tweet.created_at.year)
        Day.append(weekday[str(tweet.created_at.weekday())])
        Total_engagement.append((tweet.favorite_count+tweet.retweet_count))
        Month.append(tweet.created_at.month)
        Like.append(tweet.favorite_count)
        Love.append(0)
        Wow.append(0)
        Haha.append(0)
        Angry.append(0)
        Thankful.append(0)
        Comment.append(0)
        Share.append(tweet.retweet_count)
        Dislike.append(0)
        Views.append(0)
        Genre.append(0)
        Full_text.append(str(tweet.full_text))
        Time_stamp.append(tweet.created_at)
        Time.append(set_timeband(tweet.created_at.hour))
        
        
        
        
        
    df_final=pnd.DataFrame()
    df_final=df_final.assign(Fk_id=Fk_id).assign(Name=Name).assign(Platform=Platform).assign(Post_id=Post_id).assign(Link=Link).assign(Type=Type).assign(Year=Year)
    df_final=df_final.assign(Day=Day).assign(Total_engagement=Total_engagement).assign(Month=Month).assign(Like=Like).assign(Love=Love).assign(Wow=Wow).assign(Haha=Haha)
    df_final=df_final.assign(Angry=Angry).assign(Thankful=Thankful).assign(Comment=Comment).assign(Share=Share).assign(Dislike=Dislike).assign(Views=Views)
    df_final=df_final.assign(Genre=Genre).assign(Full_text=Full_text).assign(Time_stamp=Time_stamp).assign(Time_band=Time)
    
    return df_final

def set_timeband(x):
    if x>=0 and x<4 :
        return 1
    if x>=4 and x<8 :
        return 2
    if x>=8 and x<12 :
        return 3
    if x>=12 and x<16 :
        return 4
    if x>=16 and x<20 :
        return 5
    if x>=20 and x<=23 :
         return 6
    
    return 

def write_Xlbook(df):
  
  tx = t.localtime()
  timestamp = t.strftime('%b-%d-%Y_%H%M%S', tx)
  writer = pnd.ExcelWriter('Twitter Engagement metrics data- output on '+timestamp+'.xlsx')
  #writer = pnd.ExcelWriter('output.xlsx')
  try:
   df.to_excel(writer,'Sheet1')
  except pyxl.utils.exceptions.IllegalCharacterError as e:
    print('error while writng a file')

  
  writer.save()
  return


if __name__ == '__main__':
	#pass in the username of the account you want to download
        
        tw_hanle=list()
        tw_handle=read_TWpagelist()
        for h in tw_handle:
          get_all_tweets(h)
          
