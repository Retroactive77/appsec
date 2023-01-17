import shelve,backend
from flask import Flask, render_template, request,redirect,url_for,session
from flask_session import Session





app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_account_form=backend.CreateUseraccount(request.form)
    if request.method == 'POST' and create_account_form.validate():
        db = shelve.open('users','c')
        if 'key' in db:
            user_dict=db['key']
        else:
            user_dict={}

        if create_account_form.email.data in user_dict:
            print('email used')
        else:

            user_account=backend.User(create_account_form.name.data,create_account_form.email.data,create_account_form.password.data)

            user_dict[user_account.get_email()]=user_account
            db['key']=user_dict
            session['name']=user_dict[create_account_form.email.data]
            db.close()

        return redirect(url_for('data'))



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
                    return redirect(url_for('userprofile'))

                else:
                    print("password wrong")
                    #password wrong
            else:
                print("email dont exist")
                #email dont exist

        finally:
            db.close()


    return render_template('login.html',form=login_account_form)

@app.route('/forgetpassword')
def forgetp():
    forget_account_form=backend.ForgetUserpassword(request.form)
    if request.method == 'POST' and forget_account_form.validate():
         db = shelve.open('users','r')
         try:
            user_dict=db['key']
         except:
            print('empty shelve?')
         else:
            if forget_account_form.email.data in list(user_dict.keys()):
                pass#send the email
    return render_template('forgotpassword.html')

@app.route('/resetpassword')
def resetp():
    reset_password_form=backend.ResetUserpassword(request.form)
    if request.method == 'POST' and reset_password_form.validate():
        email=request.view_args['variable']
        db = shelve.open('users','c')

        user_dict=db['key']
        user=user_dict[email]
        user.set_password(reset_password_form.password.data)

        db.close()



@app.route('/index')
def data():
    users_list=backend.create_list()
    count=len(users_list)
    return render_template('index.html',count=count,users_list=users_list)

@app.route('/delete', methods=["GET","POST"])
def deleteacc():
    delete_account_form=backend.LoginUseraccount(request.form)
    if request.method == 'POST' and delete_account_form.validate():
        email=session['name'].get_email()
        password=session['name'].get_password()
        if email == delete_account_form.email.data and password == delete_account_form.password.data:
            db = shelve.open('users','c')

            user_dict=db['key']
            user_dict.pop(delete_account_form.email.data)

            db['key']=user_dict
            db.close()

            session['name']=None
            return redirect(url_for('home'))
        else:
            print('details wrong')
    return render_template('deleteaccount.html',form=delete_account_form)
@app.route('/deleteuser')
def admindeleteuser():
    pass
    #return render_template()

@app.route('/profile')
def userprofile():
    return render_template('profile.html',name=session['name'].get_username())

if __name__ == '__main__':
    app.run()
