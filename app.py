from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

oauth = OAuth(app)

github = oauth.register(
name='github',
client_id='Ov23liaihGJY0WdxxTJ49',
client_secret='7b17d699149da0533daba442c9702f0597e376f66',

access_token_url='https://github.com/login/oauth/access_token',

authorize_url='https://github.com/login/oauth/authorize',
api_base_url='https://api.github.com/',
client_kwargs={'scope': 'user:email'},
)

@app.route('/login')
def login():
    return github.authorize_redirect(url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user').json()
    session['user'] = user
    return redirect('/profile')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized", 401
    return jsonify(session['user'])
    
@app.route('/api/secure-data')
def secure_data():
    # Check if user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized Access", "message": "You must be logged in to see this secret data."}), 401
    
    # If logged in, return special data
    return jsonify({
        "status": "Success",
        "message": "Welcome to the hidden vault!",
        "secret_code": "SIA-AUTHENTICATION-PRO-2026",
        "logged_in_as": session['user'].get('login')
    })

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
