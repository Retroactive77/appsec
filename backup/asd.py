from wtforms import Form, StringField, EmailField, validators

class Create_useraccount(Form):
    name=StringField('entername',[validators.DataRequired()])
    email=EmailField('enteremail',[validators.DataRequired()])
    password=StringField('enterpassword',[validators.DataRequired()])
    repeatpassword=StringField('enterrepeatpassword',[validators.DataRequired()])
