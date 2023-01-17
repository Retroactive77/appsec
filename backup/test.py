import shelve

def create_list():
    db = shelve.open('users.db','r')
    userlist=[]
    for i in db:
        obj=(db[i.split(',')[0]])
        name=obj.get_username()
        password=obj.get_password()
        email=obj.get_email()
        user=[]
        user.append(name)
        user.append(email)
        user.append(password)
        userlist.append(user)

create_list()
