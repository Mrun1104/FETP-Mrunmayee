from flask import Flask, render_template, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
import google
import os
import random
import string

def generate_nonce(length=32):
    characters = string.ascii_letters + string.digits
    t = ''.join(random.choice(characters) for _ in range(length))
    return t
	
app = Flask(__name__, template_folder='template')
app.secret_key = 'm7558671042a7020712503p9226933968'

app.config['SERVER_NAME'] = 'localhost:5000'
oauth = OAuth(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/google/')
def google():
	GOOGLE_CLIENT_ID = os.environ.get('763754207706-b52b5nn06ajtmkpogom6g1t0u2qr4d2c.apps.googleusercontent.com')
	GOOGLE_CLIENT_SECRET = os.environ.get('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')

	nonce = generate_nonce()
	session['nonce'] = nonce
	CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
	oauth.register(
		name='google',
		client_id='763754207706-b52b5nn06ajtmkpogom6g1t0u2qr4d2c.apps.googleusercontent.com',
		client_secret='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',
		server_metadata_url=CONF_URL,
		client_kwargs={
			'scope': 'openid email profile'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	auth_url = oauth.google.create_authorization_url(redirect_uri, nonce=nonce)

	return auth_url

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    nonce = session.get('nonce')
    user = oauth.google.parse_id_token('https://oauth2.googleapis.com/token', nonce=nonce)
    print("Google User: ", user)
    return redirect('/')


if __name__ == "__main__":
	app.run(debug=True)
