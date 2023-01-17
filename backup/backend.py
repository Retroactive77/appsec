import shelve
from wtforms import Form, StringField, EmailField, PasswordField, validators,ValidationError


class CreateUseraccount(Form):
    name=StringField('entername',[validators.DataRequired()])
    email=EmailField('enteremail',[validators.DataRequired()])
    password=PasswordField('enterpassword',[validators.DataRequired()])
    repeatpassword=PasswordField('enterrepeatpassword',[validators.DataRequired(),validators.EqualTo('password',message='Passwords must match')],)


class LoginUseraccount(Form):
    email=EmailField('enteremail',[validators.DataRequired()])
    password=PasswordField('enterpassword',[validators.DataRequired()])


class ForgetUserpassword(Form):
    email=EmailField('enteremail',[validators.DataRequired()])

    def validate_email(self,field):
        if field.data not in list(user_dict.keys()):
            raise ValidationError("Email is not registered. Please try again")


class ResetUserpassword(Form):
    password=PasswordField('enterpassword',[validators.DataRequired()])
    repeatpassword=PasswordField('enterrepeatpassword',[validators.DataRequired(),validators.EqualTo('password',message='Passwords must match')],)


class User:
    def __init__(self,username,email,password):
        self.__username=username
        self.__email= email
        self.__password=password

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_username(self,username):
        self.__username=username

    def set_email(self,email):
        self.__email=email

    def set_password(self,password):
        self.__password=password


def create_list():
    try:
        db = shelve.open('users','r')
    except:
        print('error')
    else:
        user_dict=db['key']
        listofusers=list(user_dict.values())
        db.close()
        return listofusers
