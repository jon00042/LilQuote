import re
import sqlalchemy
import db.data_layer as db
from flask import Flask, session, request, redirect, render_template, flash, url_for

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

@app.route('/')
def index():
    show_create = True
    if ('filter_user_id' in session):
        db_quotes = db.get_all_quotes_for(session['filter_user_id'])
        del session['filter_user_id']
        show_create = False
    else:
        db_quotes = db.get_all_quotes()
    return render_template('index.html', quotes=db_quotes, show_create=show_create)

@app.route('/create_quote', methods=['POST'])
def create_quote():
    db.create_quote(session['user_id'], request.form['content'])
    return redirect(url_for('index'))

@app.route('/delete_quote/<quote_id>')
def delete_quote(quote_id):
    db.delete_quote(quote_id)
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    user_filter = request.form['user_filter']
    if (len(user_filter) <= 0):
        return redirect(url_for('index'))
    db_users = db.search_by_user_or_email(user_filter)
    if (len(db_users) <= 0):
        return redirect(url_for('index'))
    return render_template('search_results.html', users=db_users)

@app.route('/user_quotes/<user_id>')
def user_quotes(user_id):
    session['filter_user_id'] = user_id
    return redirect(url_for('index'))

@app.route('/register_form')
def register_form():
    if ('user_id' in session):  # in case someone navigates manually
        return redirect(url_for('index'))
    return render_template('register_form.html')

@app.route('/login_form')
def login_form():
    if ('user_id' in session):  # in case someone navigates manually
        return redirect(url_for('index'))
    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login():
    if (len(request.form['email']) <= 0 or len(request.form['password']) <= 0):
        flash('login fields cannot be empty!')
        return redirect(url_for('login_form'))
    user = None
    try:
        user = db.get_user_by_email(request.form['email'])
    except sqlalchemy.orm.exc.NoResultFound:
        flash('failed login attempt!')
    except Exception as ex:
        flash('internal error: {}'.format(ex))
    if (user is None):
        return redirect(url_for('login_form'))
    if (user.password != request.form['password']):
        flash('failed login attempt!')
        return redirect(url_for('login_form'))
    session['user_id'] = user.id
    session['fullname'] = user.fullname
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    is_valid = True
    for field in [ 'email', 'fullname', 'password' ]:
        if (len(request.form[field]) <= 0):
            flash('{} cannot be empty!'.format(field))
            is_valid = False
    if (request.form['password'] != request.form['confirm']):
        flash('passwords do not match!')
        is_valid = False
    if (not is_valid):
        return redirect(url_for('register_form'))
    user = None
    try:
        user = db.create_user(request.form['email'], request.form['fullname'], request.form['password'])
    except sqlalchemy.exc.IntegrityError:
        flash('email address already registered!')
    except Exception as ex:
        flash('internal error: {}'.format(ex))
    print('user: {}'.format(user))
    if (user is None):
        return redirect(url_for('register_form'))
    session['user_id'] = user.id
    session['fullname'] = user.fullname
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

app.run(debug=True)

