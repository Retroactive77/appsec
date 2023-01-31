import shelve,backend
from flask import Flask, render_template, request,redirect,url_for,session
from flask_session import Session





app = Flask(__name__,static_folder='static')


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    if session['loggedin']==True:
        return render_template('home.html',session=session['loggedin'],name=session['name'].get_username())
    return render_template('home.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session['loggedin']==True:
        return redirect(url_for('userprofile'))
    create_account_form=backend.CreateUseraccount(request.form)
    if request.method == 'POST' and create_account_form.validate():
        db = shelve.open('users','c')
        if 'key' in db:
            user_dict=db['key']
        else:
            user_dict={}

        if create_account_form.email.data in user_dict:
            return render_template('signup.html',form=create_account_form,emailused="Email is already in use")
        else:

            user_account=backend.User(create_account_form.name.data,create_account_form.email.data,create_account_form.password.data)

            user_dict[user_account.get_email()]=user_account
            db['key']=user_dict
            session['name']=user_dict[create_account_form.email.data]
            session['loggedin']=True
            db.close()

        return redirect(url_for('home'))



    return render_template('signup.html',form=create_account_form)

@app.route('/login', methods=["GET","POST"])
def login():
    login_account_form=backend.LoginUseraccount(request.form)
    if request.method == 'POST' and login_account_form.validate():

        db = shelve.open('users','r')
        try:
            user_dict=db['key']
        except:
            print('empty shelve?')

        else:
            if login_account_form.email.data in list(user_dict.keys()):
                if login_account_form.password.data == user_dict[login_account_form.email.data].get_password():
                    session['name']=user_dict[login_account_form.email.data]
                    session['loggedin']=True
                    return redirect(url_for('userprofile'))

                else:
                    print("password wrong")
                    return render_template('login.html',form=login_account_form,perror="Password is incorrect.")
            else:
                print("email dont exist")
                return render_template('login.html',form=login_account_form,merror="Email is not registered.")

        finally:
            db.close()


    return render_template('login.html',form=login_account_form)


@app.route('/logout')
def logout():
    session['loggedin']=False
    session['name']=None
    return redirect(url_for('home'))

@app.route('/forgetpassword',methods=["GET","POST"])
def forgetp():
    if session['loggedin']==True:
        return redirect(url_for('resetp'))
    forget_account_form=backend.ForgetUserpassword(request.form)
    if request.method == 'POST' and forget_account_form.validate():
         db = shelve.open('users','r')
         try:
            user_dict=db['key']
         except:
            print('empty shelve?')
         else:
            if forget_account_form.email.data in list(user_dict.keys()):
                user_dict[forget_account_form.email.data].set_password('123')
                db['key']=user_dict
                session['name']=user_dict[forget_account_form.email.data]
                db.close()
                return redirect(url_for('login'))
            else:
                db.close()
                return render_template('forgotpassword.html',form=forget_account_form,wemail='Email is not registered')
    return render_template('forgotpassword.html',form=forget_account_form)

@app.route('/resetpassword', methods=["GET","POST"])
def resetp():
    if session['loggedin']==False:
        return redirect(url_for('forgetp'))
    reset_password_form=backend.ResetUserpassword(request.form)
    if request.method == 'POST' and reset_password_form.validate():

        email=session['name'].get_email()
        db = shelve.open('users','c')

        user_dict=db['key']
        user=user_dict[email]
        user.set_password(reset_password_form.newpassword.data)
        user_dict[email]=user
        db['key']=user_dict
        db.close()
        session['name']=user

        return redirect(url_for('userprofile'))


    return render_template('resetpassword.html',form=reset_password_form,session=session['loggedin'],name=session['name'].get_username())



@app.route('/index')
def data():
    session['index']=True
    users_list=backend.create_list()
    count=len(users_list)
    if session['loggedin']==True:
        return render_template('index.html',count=count,users_list=users_list,session=session['loggedin'],name=session['name'].get_username())
    return render_template('index.html',count=count,users_list=users_list)

@app.route('/delete', methods=["GET","POST"])
def deleteacc():
    email=session['name'].get_email()

    db = shelve.open('users','c')

    user_dict=db['key']
    user_dict.pop(email)

    db['key']=user_dict
    db.close()

    session['name']=None
    session['loggedin']=False

    return redirect(url_for('home'))

@app.route('/deleteuser/<user>')
def admindeleteuser(user):

    if session['name'].get_email()==user:
        session['loggedin']=False
        session['name']=None

    db = shelve.open('users','c')
    user_dict=db['key']
    user_dict.pop(user)

    db['key']=user_dict
    db.close()

    return redirect(url_for('data'))

@app.route('/profile')
def userprofile():
    if session['loggedin']==False:
        return redirect(url_for('home'))
    return render_template('profile.html',session=session['loggedin'],name=session['name'].get_username(),email=session['name'].get_email(),pword=session['name'].get_password())

if __name__ == '__main__':
    app.run()
