import shelve,backend
from flask import Flask, render_template, request,redirect,url_for



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_account_form=backend.Create_useraccount(request.form)
    if request.method == 'POST' and create_account_form.validate():

        db = shelve.open('users','c')
        try:
            user_dict=db['key']
        except:
            print('empty shelve?')
            user_dict={}


        user_account=backend.User(create_account_form.name.data,create_account_form.email.data,create_account_form.password.data)



        user_dict[user_account.get_email()]=user_account
        db['key']=user_dict

        db.close()

        return redirect(url_for('data'))



    return render_template('main.html',form=create_account_form)

@app.route('/login', methods=["GET","POST"])
def login():
    login_account_form=backend.Login_useraccount(request.form)
    if request.method == 'POST' and login_account_form.validate():

        db = shelve.open('users','r')
        try:
            user_dict=db['key']
        except:
            print('empty shelve?')

        else:
            if login_account_form.email.data in list(user_dict.keys()):
                if login_account_form.password.data == user_dict[login_account_form.email.data].get_password():
                    return redirect('userprofile/'+login_account_form.email.data)
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
def resetp():
    reset_account_form=backend.Reset_useraccount(request.form)
    if request.method == 'POST' and reset_account_form.validate():
         db = shelve.open('users','r')
         try:
            user_dict=db['key']
         except:
            print('empty shelve?')

         else:
            if login_account_form.email.data in list(user_dict.keys()):
                pass


@app.route('/index')
def data():
    users_list=backend.create_list()
    count=len(users_list)
    return render_template('index.html',count=count,users_list=users_list)

@app.route('/updateUser/<email>')
def adminchangeuser():
    return render_template()

@app.route('/profile/<email>')
def userprofile():
    return

if __name__ == '__main__':
    app.run()
