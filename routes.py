from werkzeug.utils import redirect
from newsapplication import app
from flask import render_template, request
from .crud import *
from .voice import *

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index(categoryprovided=None):

    title=[]
    category=[]
    description=[]
    newscontent=[]
    newsimage=[]
    newsurl=[]
    newsidlist=[]
    if categoryprovided!=None:
        allnews=readNewsByCategory(categoryprovided)
    else:
        allnews=readNews()
    curr_user = session.get('email')
    #userlist=[]

    for i in range(len(allnews)):
        title.append(allnews[i].to_dict().get("title"))
        category.append(allnews[i].to_dict().get("category"))
        description.append(allnews[i].to_dict().get("description"))
        newscontent.append(allnews[i].to_dict().get("newscontent"))
        newsimage.append(allnews[i].to_dict().get("urltoimage"))
        newsidlist.append(allnews[i].id)
        #userlist.append(curr_user)
        if(allnews[i].to_dict().get("newsurl")):
            newsurl.append(allnews[i].to_dict().get("newsurl"))
        else:
            newsurl.append("www.google.com")
        
    
    newslist=zip(title, newscontent, newsimage, description,newsurl,newsidlist)
    
    if curr_user:
        return render_template('home.html', newslisttoshow=newslist)
    return render_template('index.html', newslisttoshow=newslist)

@app.route('/login', methods=['GET', 'POST'])
def login():
    context=""
    if session.get('email'):
        print("session is not cleared for "+str( session.get('email')))
        return index()
    if(request.method=='POST'):
        email=request.form.get("email")
        password=request.form.get("password")
        isvaliduser=authenticateUser(email, password)
        if(isvaliduser):
            session['email']=email
            return index()
        else:
            return render_template('login.html',context="Invalid email address or password")
    return render_template('login.html')

#Signup Function
@app.route('/userregister',methods=['GET','POST'])
def signup():
    print(request.endpoint)
    if session.get('email'):
        print("please logout before registering new user "+str( session.get('email')))
        return index()
    if(request.method == 'POST'):
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password") 
        accountcreated=createUser(name,email,password)
        if(accountcreated):
            return render_template("login.html",context="Account has been created. To login put your credentials again")
        else:
            return render_template("userregister.html",context="Error occured while creating the account")
            
    return render_template("userregister.html")

@app.route('/newsbycategory', methods=['GET', 'POST'])
def newsbycategory():
    category=request.args.get("category")
    return index(category)

@app.route('/archive', methods=['GET', 'POST'])
def archive():
    return render_template('archive.html')


@app.route('/bookmark', methods=['GET', 'POST'])
def bookmark():
    
    if(request.method == 'GET'):
        title=[]
        category=[]
        description=[]
        newscontent=[]
        newsimage=[]
        newsidlist=[]
        newsurl=[]
        allnews=readNews()
        curr_user = session.get('email')
        bookmarks=readbookmarks(curr_user)
        print(bookmarks.to_dict())
        newsobjects=[]
        print("current user is "+str(curr_user))

        if curr_user is None:
            print("now render the sign up page")
            return render_template("login.html")
        else:
            newsobjects = bookmarks.to_dict().get("newsid")
            
            print("news object added to the list"+str(newsobjects))
        
            for j in range(len(newsobjects)):
                curr_newsid = newsobjects[j]
            
                for i in range(len(allnews)):
                    if(allnews[i].id==curr_newsid):
                        title.append(allnews[i].to_dict().get("title"))
                        category.append(allnews[i].to_dict().get("category"))
                        description.append(allnews[i].to_dict().get("description"))
                        newscontent.append(allnews[i].to_dict().get("newscontent"))
                        newsimage.append(allnews[i].to_dict().get("urltoimage"))
                        newsidlist.append(allnews[i].id)
                        newsurl.append(allnews[i].to_dict().get("newsurl"))
                        
                newslist=zip(title, newscontent, newsimage, description,newsidlist,newsurl)
                print("news list is ready")
                
            return  render_template("bookmark.html", newslisttoshow=newslist)  
    else:
        title=[]
        category=[]
        description=[]
        newscontent=[]
        newsimage=[]
        newsidlist=[]
        newsurl=[]
        allnews=readNews()
        curr_user = session.get('email')
        bookmarks=readbookmarks(curr_user)
        print(bookmarks.to_dict())
        newsobjects=[]
        print("current user is "+str(curr_user))

        if curr_user is None:
            print("now render the sign up page")
            return render_template("login.html")
        else:
            newsobjects = bookmarks.to_dict().get("newsid")
            
            print("news object added to the list"+str(newsobjects))
        
            for j in range(len(newsobjects)):
                curr_newsid = newsobjects[j]
            
                for i in range(len(allnews)):
                    if(allnews[i].id==curr_newsid):
                        title.append(allnews[i].to_dict().get("title"))
                        category.append(allnews[i].to_dict().get("category"))
                        description.append(allnews[i].to_dict().get("description"))
                        newscontent.append(allnews[i].to_dict().get("newscontent"))
                        newsimage.append(allnews[i].to_dict().get("urltoimage"))
                        newsidlist.append(allnews[i].id)
                        newsurl.append(allnews[i].to_dict().get("newsurl"))
                        
                newslist=zip(title, newscontent, newsimage, description,newsidlist,newsurl)
                print("news list is ready")

                #render_template("bookmark.html", newslisttoshow=newslist)    
            for i in range(len(title)):
                print("playing audio for "+str(title[i]))
                synthesize_text(title[i]) 
                
            return  render_template("bookmark.html", newslisttoshow=newslist)  
                    
        return render_template("bookmark.html") 

@app.route('/bookmarkWithVoice',methods=['POST'])
def bookmarkWithVoice():

    if(request.method == 'GET'):
        title=[]
        category=[]
        description=[]
        newscontent=[]
        newsimage=[]
        newsidlist=[]
        allnews=readNews()
        curr_user = session.get('email')
        bookmarks=readbookmarks(curr_user)
        print(bookmarks.to_dict())
        newsobjects=[]
        print("current user is "+str(curr_user))

        if curr_user is None:
            print("now render the sign up page")
            return render_template("login.html")
        else:
            newsobjects = bookmarks.to_dict().get("newsid")
            
            print("news object added to the list"+str(newsobjects))
        
            for j in range(len(newsobjects)):
                curr_newsid = newsobjects[j]
            
                for i in range(len(allnews)):
                    if(allnews[i].id==curr_newsid):
                        title.append(allnews[i].to_dict().get("title"))
                        category.append(allnews[i].to_dict().get("category"))
                        description.append(allnews[i].to_dict().get("description"))
                        newscontent.append(allnews[i].to_dict().get("newscontent"))
                        newsimage.append(allnews[i].to_dict().get("urltoimage"))
                        newsidlist.append(allnews[i].id)
                        
                newslist=zip(title, newscontent, newsimage, description,newsidlist)
                print("news list is ready")

                #render_template("bookmark.html", newslisttoshow=newslist)    
            for i in range(len(title)):
                print("playing audio for "+str(title[i]))
                #synthesize_text(title[i]) 
                
            return  render_template("bookmarkWithVoice.html", newslisttoshow=newslist)  
            
    return  render_template("bookmarkWithVoice.html") #, newslisttoshow=newslist) 
    
@app.route('/saveBookmark',methods=['POST'])
def saveBookmark():
    newsid=request.form.get("book")
    curr_user = session.get('email')
    if curr_user is None:
        print("now render the sign up page")
        return render_template("userregister.html")
    else:
        print(str(newsid)+" getting the newsid from bookmark action for "+ str(curr_user))
        if not firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json') 
            firebase_admin.initialize_app(cred)
        db=firestore.client()
                
        data={"newsid":newsid} #,"email":curr_user}
        print("data "+str(data))
        if db.collection("bookmarks").document(curr_user).get().exists:
            doc_name = db.collection("bookmarks").document(curr_user)
            doc_name.update({
                'newsid': firestore.ArrayUnion([newsid])
            })
            #print('Inserted second')    
        else:            
            
            db.collection("bookmarks").document(curr_user).set(data)
            #print("inserted first")
        

        print("saved in db now")
        return index() #render_template("bookmark.html")

@app.route('/signout', methods=['GET', 'POST'])
def logout():
    context=""
    if(request.method=='GET'):
        isLoggedOut = session.pop('email')
        if(isLoggedOut):
            print("Successfully Logged out!!")
            return index()
        else:
            return render_template('index.html',context="Error while Logging the User out")
    
    #print("signout get method")
    return render_template('index.html')