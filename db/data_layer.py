from sqlalchemy import or_, and_
from db.base import DbManager
from db.entities import User, Quote

db = DbManager()

def get_all_quotes():
    pass

def get_all_quotes_for(user_id):
    pass

def search_by_user_or_email(query):
    return db.open().query(User).filter(or_(User.fullname.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()

def create_quote(user_id, content):
    pass

def delete_quote(quote_id):
    pass

def get_user_by_id(user_id):
    pass

def get_user_by_name(fullname):
    pass

def get_user_by_email(email):
    return db.open().query(User).filter(User.email == email).one();

def create_user(email, fullname, password):
    user = User()
    user.email = email
    user.fullname = fullname
    user.password = password
    db.save(user)
    return user


