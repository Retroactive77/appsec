#loginpage,userprofile,editinformatiom,admin,adminuserlist,userpermissionsonuserinfo,publicdisplayofuserprofile
from flask import Flask, render_template, request,redirect,url_for,session,make_response
from flask_session import Session
import backend
import os,ssl

import firebase_admin
from firebase_admin import credentials,db,firestore,auth

import pyrebase


config = {
  "apiKey": "AIzaSyD0SUfjgpcMolK-chcXdqfLMGvumxfTTPU",
  "authDomain": "appsec-20fc0.firebaseapp.com",
  "databaseURL": "https://appsec-20fc0-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "appsec-20fc0.appspot.com"
}

firebase = pyrebase.initialize_app(config)

cred = credentials.Certificate("certificates/appsec-20fc0-firebase-adminsdk-nrz0d-6ddcefb057.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__,static_folder='static')
app.secret_key = os.path.join(os.path.dirname(__file__), 'certificates', 'key.pem')

cert_path = os.path.join(os.path.dirname(__file__), 'certificates', 'cert.pem')
key_path = os.path.join(os.path.dirname(__file__), 'certificates', 'key.pem')

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(cert_path, key_path)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
Session(app)

pauth=firebase.auth()

@app.after_request
def add_security_headers(response):
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' cdn.example.com;"
    return response

@app.route('/')
def home():

    return render_template('homepg.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
            return redirect(url_for('home'))
    if request.method == 'POST':

        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        print(name,email,password)

        try:
            pauth.create_user_with_email_and_password(email, password)
            pauth.send_email_verification(email)
        except pyrebase.pyrebase.HTTPError as e:
            error_message = e.args[1]['error']['message']
            if error_message == 'EMAIL_EXISTS':
                print("Email address is already in use.")
            elif error_message == 'INVALID_EMAIL':
                print("Invalid email address format.")
            elif error_message == 'WEAK_PASSWORD':
                print("Weak password. It should be at least 6 characters long.")
            elif error_message == 'INVALID_PHONE_NUMBER':
                print("Invalid phone number format.")
            elif error_message == 'USER_DISABLED':
                print("The user account has been disabled by an administrator.")
            elif error_message == 'TOO_MANY_ATTEMPTS_TRY_LATER':
                print("Too many sign-up attempts. Please try again later.")
            else:
                print("An unknown error occurred:", error_message)

        else:
            db = firebase.database()
            data = {
                "name":name,
                "email":email
            }

            decoded_token = auth.verify_id_token(user['idToken'])
            uid = decoded_token['uid']
            results = db.child("users").child(uid).push(data,user['idToken'])

            session['name']=name
            session['email']= email

            print('something')

        return redirect(url_for('home'))



    return render_template('signup.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password= request.form.get('password')

        try:
            user = pauth.sign_in_with_email_and_password(email, password)
        except:
            print('wrong credentials')
        else:
            decoded_token = auth.verify_id_token(user['idToken'])
            uid = decoded_token['uid']

            info = db.child('users').child(uid).get()

            session['name'] = info['name']
            session['email'] = info['email']


            print(pauth.get_account_info(user['idToken']))
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/forgetpassword',methods=["GET","POST"])
def forgetp():
    forget_account_form=backend.ForgetUserpassword(request.form)
    if request.method == 'POST' and forget_account_form.validate():
        email=forget_account_form.email.data
        pauth.send_password_reset_email(email)
    return render_template('forgotpassword.html',form=forget_account_form)

@app.route('/changepassword', methods=["GET","POST"])
def resetp():
    if session['loggedin']==False:
        return redirect(url_for('forgetp'))
    reset_password_form=backend.ResetUserpassword(request.form)
    if request.method == 'POST' and reset_password_form.validate():
        try:
            pauth.sign_in_with_email_and_password(session['user'], reset_password_form.oldpassword.data)
        except KeyError:
            return render_template('resetpassword.html',form=reset_password_form,passw="Password(s) do not meet requirements.")

        return redirect(url_for('userprofile'))


    return render_template('resetpassword.html',form=reset_password_form,name=session['user'])



@app.route('/index')
def data():
    if session['admin']!=True:
        return redirect(url_for('home'))
    users_list=backend.create_list()
    count=len(users_list)
    if session['loggedin']==True:
        return render_template('index.html',count=count,users_list=users_list)
    return render_template('index.html',count=count,users_list=users_list)

@app.route('/delete', methods=["GET","POST"])
def deleteacc():
    try:
        password=0
        if 'tokenid' in user and password==password:
            session.clear()
    finally:
        return redirect(url_for('home'))

@app.route('/deleteuser/<user>')
def admindeleteuser(user):
    if session['name']!=None:
        if session['name'].get_email()==user:
            session['loggedin']=False
            session['name']=None


@app.route('/profile')
def userprofile():
    return render_template('profile.html')

@app.route('/create-admin')
def adminlogin():
    login_account_form=backend.LoginUseraccount(request.form)
    if request.method == 'POST' and login_account_form.validate():
        email=login_account_form.email.data
        password=login_account_form.password.data
        admin=''
        try:
            user = pauth.sign_in_with_email_and_password(email, password)
        except:
            print('wrong credentials')
        else:


            session['user']=email


            print(pauth.get_account_info(user['idToken']))
            return redirect(url_for('home'))
    return render_template('login.html',form=login_account_form)


if __name__ == '__main__':
    app.run(ssl_context=context)

