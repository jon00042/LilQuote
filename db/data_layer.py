from sqlalchemy import or_, and_
from db.base import DbManager
from db.entities import User, Quote

db = DbManager()

def get_all_quotes():
    return db.open().query(Quote).order_by(Quote.created_at.desc()).all()

def get_all_quotes_for(user_id):
    return db.open().query(Quote).filter(Quote.user_id == user_id).order_by(Quote.created_at.desc()).all()

def search_by_user_or_email(query):
    return db.open().query(User).filter(or_(User.fullname.like('%{}%'.format(query)), User.email.like('%{}%'.format(query)))).all()

def create_quote(user_id, content):
    user = db.open().query(User).filter(User.id == user_id).one()
    quote = Quote()
    quote.user = user
    quote.content = content
    db.save(quote)

def delete_quote(quote_id):
    quote = db.open().query(Quote).filter(Quote.id == quote_id).one()
    db.delete(quote)

def get_user_by_email(email):
    return db.open().query(User).filter(User.email == email).one();

def create_user(email, fullname, password):
    user = User()
    user.email = email
    user.fullname = fullname
    user.password = password
    db.save(user)
    return user

