import random, string
from flask import Flask, render_template, request, jsonify, make_response, redirect

online_users = {}

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + '0123456789') for i in range(length))

def auth(l, p):
    return l == p

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account/<token>")
def about(token):
    if token in online_users:
        return render_template('account.html', login=online_users[token][0])
    return 'Ты даун'
    

@app.route('/login', methods=['POST'])
def hello():
    login = request.form['login']
    password = request.form['password']

    global online_users

    if auth(login, password):
        h = generate_random_string(64)
        online_users[h] = [login, password]
        return {'success': True, 'token': h}
    else:
        return {'success': False}

if __name__ == "__main__":
    app.run(debug=True)