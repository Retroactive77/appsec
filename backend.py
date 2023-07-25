from wtforms import Form, StringField, EmailField, PasswordField, validators
import jwt
import datetime

def refresh_token():
    if 'user' in session:
        try:
            if backend.token_has_expired(user['tokenid']):
                user = auth.refresh(user['refreshToken'])
        except:
            session.clear()

def token_has_expired(token):
    try:
        decoded_token = jwt.decode(token, verify=False)  # Decode the token without verification
        expiration_timestamp = decoded_token['exp']  # Extract the expiration timestamp from the decoded token
        current_timestamp = datetime.datetime.utcnow().timestamp()  # Get the current UTC timestamp

        # Compare the current timestamp with the expiration timestamp
        if current_timestamp >= expiration_timestamp:
            return True  # Token has expired
        else:
            return False  # Token is still valid

    except jwt.ExpiredSignatureError:
        return True  # Token has expired

    except jwt.InvalidTokenError:
        return True  # Token is invalid or cannot be decoded


class CreateUseraccount(Form):
    name=StringField('',[validators.DataRequired()],render_kw={"placeholder":"Enter your name"})
    email=EmailField('',[validators.DataRequired()],render_kw={"placeholder":"Enter your email"})
    password=PasswordField('',[validators.DataRequired(),validators.Length(min=8)],render_kw={"placeholder":"Enter your password"})
    repeatpassword=PasswordField('',[validators.DataRequired(),validators.EqualTo('password',message='Passwords must match')],render_kw={"placeholder":"Re-enter password"})


class LoginUseraccount(Form):
    email=EmailField('',[validators.DataRequired()],render_kw={"placeholder": "Enter your email address"})
    password=PasswordField('',[validators.DataRequired()],render_kw={"placeholder": "Enter your password"})
    admin=PasswordField('',render_kw={"placeholder": "Admin Key (Optional)"})

class ForgetUserpassword(Form):
    email=EmailField('',[validators.DataRequired()],render_kw={"placeholder": "Enter your email address"})



class ResetUserpassword(Form):
    oldpassword=PasswordField('',[validators.DataRequired()],render_kw={"placeholder": "Enter your old password"})
    newpassword=PasswordField('',[validators.DataRequired(),validators.Length(min=8)],render_kw={"placeholder": "Enter your new password"})


