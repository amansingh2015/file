    # -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:20:42 2019

@author: zeeshan.hasan
"""

import urllib3
#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup
import json
#import numpy as np
import openpyxl as pyxl
import pandas as pnd
import datetime as dt
import time as t
import certifi
import sqlite3


def read_IGpagelist():

  print("Reading XL work book")
  df = pnd.read_excel(open('input.xlsx','rb'), sheetname='Sheet1')
  #df =  df[df.Followers_Count>2000]
  #print((df['scn']))
  return df['IG_Page']

def write_Xlbook(df):
  
  tx = dt.datetime.utcnow().strftime('%Y-%m-%d_%H_%M_%S_%f')[:-3]
  #timestamp = t.strftime('%b-%d-%Y_%H%_M_%S_%s', tx)
  writer = pnd.ExcelWriter('Instagram Cotent data- output on '+tx+'.xlsx')
  #writer = pnd.ExcelWriter('output.xlsx')
  try:
   df.to_excel(writer,'Sheet1')
  except pyxl.utils.exceptions.IllegalCharacterError as e:
    print('error while writng a file')

  
  writer.save()
  return


def save_to_db(df_final):
    conn = sqlite3.connect("insta_data.db")
    df_final.to_sql("insta_table1", conn, flavor=None, schema=None, if_exists='replace', index=False, index_label=None, chunksize=None, dtype=None)
    write_Xlbook(df_final)
    conn.close()
    return

def filter_out_existing_records_in_db(df_final):
    conn = sqlite3.connect("insta_data.db")
    df_already_saved=pnd.read_sql_query("SELECT * from insta_table1", conn )
    conn.close()
    #df_final.to_sql("insta_table1", conn, flavor=None, schema=None, if_exists='append', index=False, index_label=None, chunksize=None, dtype=None)
    print("length is ",len(df_final['Link']))
    print(list(df_final))
    df_residual=df_already_saved[~df_already_saved['Link'].isin(df_final['Link'])]
    print("length is ",len(df_residual['Link']))
    df_final=df_residual.append(df_final)
    print("length is ",len(df_final['Link']))
    write_Xlbook(df_final)
    
    return df_final
    
    
#specify the url
def get_IG_data(page_list):


    df_final=fetch_short_code_data(page_list)
    write_Xlbook(df_final)
    
    return




def fetch_short_code_data(short_code_list):
    Time_stamp_list=list()
    Full_text_list=list()
    #Comments_list=list()
    Likes_list=list()
    Link_list=list()
    Video_views_list=list()
    Media_type_list=list()
    Page_name_list=list()
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    for s in short_code_list :
        
        
        response = http.request('GET', (s))
        soup = BeautifulSoup(response.data,"lxml")
        
        try:
            script = soup.findAll('script')[4].string
            #print(soup)
            script=script.replace("window._sharedData = ",'')
            script=script.replace(";",'')
            #print((script))
            try:
                data=json.loads(str(script))
            except json.JSONDecodeError as jex:
                script = soup.findAll('script')[3].string
            #print(soup)
                script=script.replace("window._sharedData = ",'')
                script=script.replace(";",'')
                data=json.loads(str(script))
                
            if 'entry_data' in data.keys():
                
                m=data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
                Page_name_list.append(m['owner']['username'])
                
                #Time_stamp_list.append(t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(m['taken_at_timestamp'])))
                
                Time_stamp_list.append(dt.datetime(*( t.localtime(m['taken_at_timestamp'])[:6])))
                try:
                    Full_text_list.append(m['edge_media_to_caption']['edges'][0]['node']['text'])
                except KeyError as kex:
                    Full_text_list.append("")
                except IndexError as iex:
                    Full_text_list.append("")
                
                #Comments_list.append(m['edge_media_to_comment']['count'])
                Likes_list.append(m['edge_media_preview_like']['count'])
                Link_list.append("https://Instagram.com/p/"+m['shortcode'])
                print(m['owner']['username'])
                #Video_views_list.append()
                
                #print("Caption is ",m['caption'])
                #print("Date is ",t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(m['date'])))
                #print("Comments is ",m['comments']['count'])
                #print("likes is ",m['likes']['count'])
                #print("Link is ","https://Instagram.com/p/"+m['code'])
             
                if m['is_video']:
                    Video_views_list.append(m['video_view_count'])
                    #print("video_views is ",m['video_views'])
                    Media_type_list.append('Video')
                else:
                    Video_views_list.append(0)
                    Media_type_list.append('Image')
        
        
        except     AttributeError as abe:
            print('Attribute Error is ',abe)
            
            #return "Broken Link"
        
        
    
    df_final=pnd.DataFrame()
    df_final=df_final.assign(Brand=Page_name_list).assign(Post_id=Link_list).assign(Link=Link_list).assign(Time_stamp=Time_stamp_list)
    df_final=df_final.assign(Type=Media_type_list).assign(Like=Likes_list)#.assign(Comment=Comments_list)
    df_final=df_final.assign(Views=Video_views_list).assign(Full_text=Full_text_list)
    
    df_final['Platform']='Instagram'
    df_final['Category']=''
    df_final['Love']=0
    df_final['Wow']=0
    df_final['Haha']=0
    df_final['Angry']=0
    df_final['Thankful']=0
    df_final['Share']=0
    df_final['Dislike']=0
    df_final['Total_engagement']=df_final['Like']+df_final['Views']
    print(type(df_final['Time_stamp']))
    #time_stamp_pd=pnd.Series(data=df_final['Time_stamp'],dtype=)
    #time_stamp_pd=pnd.Timestamp(arg=df_final['Time_stamp'])
    #print(type(time_stamp_pd))
    return df_final
     


#calling functions

page_list=read_IGpagelist()

get_IG_data(page_list)