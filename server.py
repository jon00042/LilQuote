import re
from flask import Flask, session, request, redirect, render_template, flash, url_for

import db.data_layer as db
'''
USAGE:        db.<function_name>
EXAMPLES:     db.search_by_user_or_email('Smith')
              db.search_by_user_or_email('gmail.com')
'''

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_quote', methods=['POST'])
def create_quote():
    pass

@app.route('/delete/<quote_id>')
def delete_quote(quote_id):
    pass

@app.route('/search')
def search():
    return redirect(url_for('search_users', query=request.args['html_query']))
    
@app.route('/results/<query>')
def search_users(query):
    pass

@app.route('/user/<user_id>')
def user_quotes(user_id):
    pass

@app.route('/authenticate')
def authenticate():
    pass

@app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/logout')
def logout():
    pass

def setup_web_session(user):
    pass


app.run(debug=True)