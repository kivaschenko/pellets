# import built-in libraries
import functools
from datetime import datetime

# third party imports
import psycopg2
from flask import (
    request,
    session,
    render_template,
    redirect,
    jsonify,
    flash,
    g,
    url_for,
    Blueprint
)
from werkzeug.exceptions import abort 
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
# import from the app
from config import db_params

#======================
# CONSTANTS
INCOMING_DATE_FMT ='%Y-%m-%d %H:%M:%S'

bp = Blueprint('auth', __name__, static_folder='static', url_prefix='/auth')

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor as cur:
                cur.execute('''SELECT id, username, email
                    FROM users
                    WHERE id = %s''', (user_id,))
                query = cur.fetchone()
                g.user = {
                    'user_id': query[0], 
                    'username': query[1], 
                    'email': query[2]
                }


@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        print('form: ', request.form)
        username = request.form['InputFullname']
        email = request.form['InputEmail']
        password = request.form['InputPassword']
        agree_terms = request.form['agreeCheck']
        if agree_terms:
            with psycopg2.connect(**params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'SELECT id FROM users WHERE username=%s', (username,))
                    id = cur.fetchone()
                    if id is not None:
                        error = 'Користувач {} вже існує.'.format(username)
                    if error is None:
                        # create new user
                        cur.execute(
                            """ INSERT INTO users 
                            (username, email, password_hash) 
                                VALUES (%s, %s, %s)""", 
                                (username, email, 
                                generate_password_hash(password)))       
                        flash('Дякуємо за реєстрацію.')
                        return redirect(url_for('auth.login'))
        else:
            error = "Надо принять условия использования."
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print('request: ', request)
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        error = None
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT id, password_hash 
                FROM users WHERE username = %s""", (username,))
                user = cur.fetchone()
                if user is None:
                    error = 'Incorrect username.'
                else:
                    password_hash =  user[1]
                    if not check_password_hash(password_hash, password):
                        error = 'Incorrect password.'
                if error is None:
                    session.clear()
                    session['user_id'] = user[0]
                    return redirect(url_for('home'))
        flash(error)
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view