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

url_comments="https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&key=AIzaSyCczxRDJ0gK4DVPWZKbTPmAnUetGC1qpzk&videoId="

temp=""
videoid_list=list()
commentid_list=list()
#like_count_list=list()
#view_count_list=list()
#dislike_count_list=list()
#comment_count_list=list()
time_count_list=list()
comment_text_list=list()
description=list()
#duration=list()
author_list=list()

def read_YT_pagelist():
    print("Reading XL work book")
    df = pnd.read_excel(open('input_vidid.xlsx','rb'), sheet_name='input')
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
    writer = pnd.ExcelWriter('YT comments data- output on '+timestamp+'.xlsx')
    #writer = pnd.ExcelWriter('output.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    return


def get_YT_subcount(page_name,df_final):
    count=0
    for page in page_name:
        i=1
        #print(url_1,page)
        #data1=requests.get((url_1+page)).json()
        #if data1['totalResults']==0 :
        #    continue
        #videoid_list.append(page)

        data = requests.get((url_comments+page)).json()
        next_page_token=''
        print(page)
        while i:
            try:
                data = requests.get((url_comments+page+"&pageToken="+next_page_token)).json()
                next_page_token=data['nextPageToken']
            except Exception as kex:
                print('Excption is e',kex )
                i=0
            try:
                
                    
                    
                
                for item in data['items']:
                    if 'replies' in item:
                        print("in replies part")
                        #print(item['replies']['comments'][0].keys())
                        for reply_item in item['replies']['comments']:
                            count+=1
                            #print(reply_item['snippet'].keys())
                            videoid_list.append(page)
                            time_count_list.append(reply_item['snippet']['publishedAt'])
                            comment_text_list.append(reply_item['snippet']['textOriginal'])
                            author_list.append(reply_item['snippet']['authorDisplayName'])
                            #print('idis ',reply_item['id'])
                            commentid_list.append(reply_item['id'])
                            print("Counter is ",count)
                        
                
                    count+=1
                    #print((item['snippet']['topLevelComment']['snippet']).keys())
                    #print(item['snippet']['topLevelComment']['id'])
                    print("Counter is ",count)
                    #print(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    #print(item['snippet']['topLevelComment']['snippet']['textOriginal'])
                    #print(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                    videoid_list.append(page)
                    time_count_list.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                    comment_text_list.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
                    author_list.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    commentid_list.append(item['snippet']['topLevelComment']['id'])
                    #duration=list()
            except KeyError as keyex:
                if 'items' in str(keyex):
                    break
            #print(url_comments+page+"&pageToken="+next_page_token)    
            
            #print("Data is",data)
                
    
    df_final=df_final.assign(Comment_ID=commentid_list).assign(Author_Name=author_list).assign(Text=comment_text_list).assign(Time_stamp=time_count_list).assign(Video_id=videoid_list)
    
    return df_final
    


    

#  Funcrtion callling 

df_final=pnd.DataFrame()
x=read_YT_pagelist()

df_final=get_YT_subcount(x,df_final)

write_Xlbook(df_final)
