from sqlalchemy import or_, and_
from db.base import DbManager
from db.entities import User, Quote

db = DbManager()

def get_all_quotes():
    pass

def get_all_quotes_for(user_id):
    pass

def search_by_user_or_email(query):
    return db.open().query(User).filter(or_(User.username.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()

def create_quote(user_id, content):
    pass

def delete_quote(quote_id):
    pass

def get_user_by_id(user_id):
    pass

def get_user_by_name(username):
    pass

def get_user_by_email(user_email):
    pass

def create_user(email, username, password):
    pass


