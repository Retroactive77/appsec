import pyrebase

config = {
    "apiKey": "AIzaSyDl-xqQ8jaApQ-Bw280tER2KYxzatYNZmg",
    "authDomain": "appsec-f8d51.firebaseapp.com",
    "databaseURL": "https://appsec-f8d51-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "appsec-f8d51.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def handle_form_submission(request):
    data = {
        "blog/"+db.generate_key():{
        "name": request.form.get("name33"),
        "title": request.form.get("title33"),
        "contents": request.form.get("contents33"),
        }
    }
    db.child("messages").push(data)

    return "Form submitted successfully!"



