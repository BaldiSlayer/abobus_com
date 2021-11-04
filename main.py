import random, string
from flask import Flask, render_template, request, jsonify, make_response, redirect

online_users = {}

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + '0123456789') for i in range(length))

def auth(l, p):
    if l == 'admin' and p == 'admin':
        return True

    return False

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account/<token>")
def about(token):
    if token in online_users:
        return render_template('managet_account.html', login=online_users[token][0])
    return 'Ошибка доступа'
    

@app.route('/order')
def order():
    return render_template('order.html')

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
        return redirect("/")

@app.route('/do_order', methods=['POST'])
def he1o():
    full_name = request.headers['Fio'] 
    email = request.headers['Email'] 
    phone_number = request.headers['Number'] 
    place = request.headers['Place'] 
    time = request.headers['Time'] 

    print(full_name, email, phone_number, place, time)

    return "Чмо ебало завали"

if __name__ == "__main__":
    app.run(debug=True)