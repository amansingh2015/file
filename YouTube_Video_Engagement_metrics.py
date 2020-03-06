'''
Created on Apr 2, 2017

@author: ank    t.mishra
'''

import requests
import os
import pandas as pnd
import time as t



url_3="https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails&key=AIzaSyCczxRDJ0gK4DVPWZKbTPmAnUetGC1qpzk&id="
url_1 = "https://www.googleapis.com/youtube/v3/channels?part=id&key=AIzaSyCczxRDJ0gK4DVPWZKbTPmAnUetGC1qpzk&id="
url_2 = "https://www.googleapis.com/youtube/v3/channels?part=statistics&key=AIzaSyCczxRDJ0gK4DVPWZKbTPmAnUetGC1qpzk&id="
temp=""
videoid_list=list()
like_count_list=list()
view_count_list=list()
dislike_count_list=list()
comment_count_list=list()
time_count_list=list()
title_list=list()
description=list()
duration=list()
author_list=list()

def read_YT_pagelist():
    print("Reading XL work book")
    df = pnd.read_excel(open('input_vidid.xlsx','rb'), sheetname='input')
    page_list=pnd.Series.dropna(df['Id'])
    
    
    return page_list


def user_Type(name,type):
    if type=="channel" :
        temp=url_2+name;
        print(temp)
             
    if type=="user" :
        temp=url_1+name;
        print(temp)
    
    return temp



def write_Xlbook(df):
    tx = t.localtime()
    timestamp = t.strftime('%b-%d-%Y_%H%M ', tx)
    writer = pnd.ExcelWriter(os.getcwd()+'YT engagement data- output on '+timestamp+'.xlsx')
    #writer = pnd.ExcelWriter('output.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    return


def get_YT_subcount(page_name,df_final):
    i=0
    for page in page_name:
        #print(url_1,page)
        #data1=requests.get((url_1+page)).json()
        #if data1['totalResults']==0 :
        #    continue
        videoid_list.append(page)

        data = requests.get((url_3+page)).json()
        i=i+1
        print (str(  page) +"   "+str(i))
        #print (str(  page +"  View count"+ data['items'][0]['statistics']['viewCount']))
        
        try:
          view_count_list.append( int(data['items'][0]['statistics']['viewCount']))
        except IndexError as ex :
            
            if (str(ex).find('dislikeCount')) :
                
                print('in dislikeCount exception handling- line 76')
                view_count_list.append(0)
        except KeyError as ex :
            view_count_list.append(0)
        
        
        try :
            dislike_count_list.append(int(data['items'][0]['statistics']['dislikeCount']))
        
        except IndexError as ex :
            print('Countered Index Error')
            dislike_count_list.append(0)
        except KeyError as ex :
            
            if (str(ex).find('dislikeCount')) :
                
                print('in dislikeCount exception handling - line 89')
                dislike_count_list.append(0)
                       
        try :
            comment_count_list.append(int(data['items'][0]['statistics']['commentCount']))                          
        
        except IndexError as ex :
            if (str(ex).find('commentCount')) :
                print('in commentCount exception handling line 97')
                comment_count_list.append(0)
        except KeyError as ex :
            if (str(ex).find('commentCount')) :
                print('in commentCount exception handling line 97')
                comment_count_list.append(0)
                
        try :
            like_count_list.append(int(data['items'][0]['statistics']['likeCount']))                         
        
        except IndexError as ex :
            if (str(ex).find('likeCount')) :
                print('in likeCount exception handling')
                like_count_list.append(0)
        except KeyError as ex :
            if (str(ex).find('likeCount')) :
                print('in likeCount exception handling')
                like_count_list.append(0)
        author_list.append(data['items'][0]['snippet']['channelTitle'])
##
##        try :
##            duration.append(int(data['items'][0]['contentDetails']['duration']))                         
##        
##        except KeyError as ex :
##            if (str(ex).find('duration')) :
##                print('in duration exception handling')
##                like_countduration_list.append(0)        
##                
##                
##                    
                
                
        try:    
            time_count_list.append(data['items'][0]['snippet']['publishedAt'])
        except IndexError as ex :
             time_count_list.append(0)
        try:    
            title_list.append(data['items'][0]['snippet']['title'])
        except IndexError as ex :
            title_list.append(0)
        try:    
            description.append(data['items'][0]['snippet']['description'])
        except IndexError as ex :
            description.append(0) 
        try:    
            duration.append(data['items'][0]['contentDetails']['duration'])
        except IndexError as ex :
            duration.append(0) 
                

        print('length of video ID',len(videoid_list),'length of Like Count',len(like_count_list),'length of View Count',len(view_count_list))
        print('length of Dislike Count',len(dislike_count_list),'length of Comment Count',len(comment_count_list))
        print('length of Time ',len(time_count_list))
        print('Title -',len(title_list),'Description -',len(description))
        
        df_final=df_final.assign(Author=author_list).assign(Video_ID=videoid_list).assign(Time=time_count_list).assign(Video_Title=title_list).assign(Description= description)
        df_final=df_final.assign(Likes=like_count_list).assign(Comments=comment_count_list).assign(Dislike=dislike_count_list).assign(Views=view_count_list).assign(Duration=duration)
        write_Xlbook(df_final)
        df_final=pnd.DataFrame()
            
                  
        
        #subscriber_count_list.append(data['items'][0]['statistics']['subscriberCount'])
    
    
    
    return df_final
    
    

#  Funcrtion callling 

df_final=pnd.DataFrame()
x=read_YT_pagelist()

df_final=get_YT_subcount(x,df_final)

#write_Xlbook(df_final)

