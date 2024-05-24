#from newsapplication import app
from newsapi import NewsApiClient
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




newsapi1=NewsApiClient(api_key="0a4f5b37a1494f33b759d142f50fad9d")
topheadlines=newsapi1.get_top_headlines(category="business")
articles=topheadlines['articles']
description=[]
title=[]
img=[]
newscontent=[]

 #Adding news to the firestore
if not firebase_admin._apps:
         cred = credentials.Certificate('serviceAccountKey.json') 
         firebase_admin.initialize_app(cred)
db=firestore.client()
for i in range(len(articles)):
    myarticles=articles[i]
    data={"title":myarticles['title'],"description":myarticles['description'],"urltoimage":myarticles['urlToImage'],"newscontent":myarticles['content'],"category":"business","date":myarticles["publishedAt"],"newsurl":myarticles["url"]}
    db.collection("News").add(data)

for i in range(len(articles)):
    print(articles[i])

print("successful")

    


        
    
