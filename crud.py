import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from newsapi import NewsApiClient
from flask import session

firebaseConfig = {
    "apiKey": "AIzaSyBkSwC2eBOfdSiaIMbAZ321tnnyzFq7GWQ",
  "authDomain": "userdata-ad8b3.firebaseapp.com",
  "projectId": "userdata-ad8b3",
  "storageBucket": "userdata-ad8b3.appspot.com",
  "messagingSenderId": "822647666262",
  "appId": "1:822647666262:web:bfc4d5dea2ee28b2482df7",
  "databaseURL":""
                  }
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()        

def authenticateUser(email,password):
    
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        session['email']=email
        return True
    except:
        return False        

def createUser(name,email,password):

    try:
        auth.create_user_with_email_and_password( email, password)
        return True
    except:
        return False
        
#Adding news to the firestore
def addNews():
    newscategory="technology"
    newsapi=NewsApiClient(api_key="0a4f5b37a1494f33b759d142f50fad9d")
    topheadlines=newsapi.get_top_headlines(category=newscategory)
    articles=topheadlines['articles']
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json') 
        firebase_admin.initialize_app(cred)
    db=firestore.client()
    for i in range(len(articles)):
        myarticles=articles[i]
        data={"title":myarticles['title'],"description":myarticles['description'],"urltoimage":myarticles['urlToImage'],"newscontent":myarticles['content'],"category":"technology","date":myarticles["publishedAt"]}
        db.collection("News").add(data)
    
#Read data
def readNews():
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json') 
        firebase_admin.initialize_app(cred)
    db=firestore.client()
    #docs=db.collection("News").where("category","==","sports").get()
    docs=db.collection("News").get()
    return docs

def readNewsByCategory(category):
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json') 
        firebase_admin.initialize_app(cred)
    db=firestore.client()
    docs=db.collection("News").where("category","==",category).get()
    return docs

def readbookmarks(curr_user):
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json') 
        firebase_admin.initialize_app(cred)
    db=firestore.client()

    #docs=db.collection("News").where("category","==","sports").get()
    docs=db.collection("bookmarks").document(curr_user).get() #.to_dict().get("newsid")
    return docs