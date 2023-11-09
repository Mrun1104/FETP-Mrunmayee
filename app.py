import email
from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import oauthlib
import pytz
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'
oauth = oauthlib(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']

google = oauth.remote_app(
    'google',
    consumer_key='763754207706-b52b5nn06ajtmkpogom6g1t0u2qr4d2c.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/gmail.readonly',
    },
    base_url='https://www.googleapis.com/gmail/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login')
def google_login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('login'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('https://www.googleapis.com/gmail/v1/users/me/profile').data

    session['email'] = user_info['emailAddress']
    session['name'] = user_info['displayName']

    return redirect(url_for('success'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)

   
    session['email'] = "email"
    session['name'] = "name"

    

@app.route('/success')
def success():
    if 'email' in session:
        return render_template('success.html')
    else:
        return redirect(url_for('login'))
    
def get_indian_time():
    india_timezone = pytz.timezone('Asia/Kolkata')
    time_in_india = datetime.datetime.now(india_timezone)
    return time_in_india.strftime('%Y-%m-%d %H:%M:%S %Z%z')



