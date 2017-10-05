#views.py

from flask import render_template,flash,session ,redirect,request,url_for
from werkzeug.utils import secure_filename
#from flask_mail import Mail,Message
import mysql.connector
from app import app
import MySQLdb
import os
#upload folder where we extract data and working on time
Upload_Folder ='/home/rsingh/mysite/backup/'
app.config['UPLOAD_FOLDER'] = Upload_Folder
#set secret key
app.secret_key = 'A9756BCD'
#create connection between mysql and python
db = MySQLdb.connect("rsingh.mysql.pythonanywhere-services.com","rsingh","golusingh","rsingh$testDb" )
curr = db.cursor()

@app.route('/')
def index():
    if 'userName' in session:
        userName = session['userName']
        return "login as :"+userName
    return render_template("index.html")


#call about html
@app.route('/about')
def about():
    return render_template("about.html")

#call login html
@app.route('/signup',methods =['GET','POST'])
def signup():
    if request.method == "POST" :
        #store in variable to work on future
        name = request.form['name']
        emailId = request.form['emailId']
        password = request.form['password']

        #insert into the user table and in future right a procedure to create seprate login and anyother specific detail
        query = "insert into user(userName,emailId,password) values ('"+name+"','"+emailId+"','"+password+"')"
        #return query
        curr.execute(query)
        db.commit()
        return render_template("login.html") 

    return render_template("signup.html")

#call forget_password
@app.route('/forgetPassword')
def forgetPassword():
    return render_template("forgetPassword.html")

#show userInformation
@app.route('/userDetail')
def userDetail():
    return render_template("userInfo.html")

#show signup information
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['userName'] = request.form["username"]
        curr.execute("select count(*) from user where emailId = '"+format(request.form['username'])+"'")
        
        if not curr.fetchone()[0]:
                return 'Invalid username'
        curr.execute("select count(*) from user where password ={} ;".format(request.form['password']))
        if not curr.fetchone()[0]:
                return 'Invalid password'
        return render_template("userInfo.html")

        #if request.form['username'] != 'admin@gmail.com' and request.form['password'] != '12345':
        #    return render_template("inValid.html")
        #else:
        #    return render_template("userInfo.html")
    return render_template("login.html")
#show Invalid information
#show logout detail

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('userName',None)
    return redirect(url_for('index'))

#check that upload function work here or
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file upload')
            return "so main problem is hjere"
            return render_template("upload.html")
        else:
            f = request.files['file']
            fileName = secure_filename(f.filename)
            #return "File is here",filename
            #f.save(secure_filename(f.filename))
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            #fp = open(os.path.join(app.config['UPLOAD_FOLDER'],fileName),"rb")
            sql = "insert into fileData(file,type,file_name) values (?,?,?)"
            try:
                curr.execute(sql,[LOAD_FILE(fileName),'json',fileName])
                db.commit()
                return "file Submmitted successfully"
            except Exception:
                return "file Not submitted into db :"
    return render_template("upload.html")
#insert the method related to test
#show when the user final start test then this function is going to work its mainly use to serve the page
#online

@app.route('/test',methods=['GET','POST'])
def test():
    curr.execute("select * from testSet")
    rows = curr.fetchall()
    return render_template('test.html',rows=rows)
    #request for login without login send user to signup page
    return "welcome to the test page"


#this page show the content of the different test and also show that some number of detail about that 
#each time you got new question may be repated





#this function is going to start test subject wise
