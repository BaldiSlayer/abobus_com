import random, string
from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy

online_users = {}

USERS = {"admin": "admin"}

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + '0123456789') for i in range(length))

def auth(l, p):
    if l == 'admin' and p == 'admin':
        return True

    return False

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order.db'
db_order = SQLAlchemy(app)

class Order(db_order.Model):
    id = db_order.Column(db_order.Integer, primary_key=True, autoincrement=True)
    full_name = db_order.Column(db_order.String(322))
    email = db_order.Column(db_order.String(322))
    phone_number = db_order.Column(db_order.String(322))
    place = db_order.Column(db_order.String(322)) #нужно переделать
    time = db_order.Column(db_order.String(322)) #переделать в int
    manager = db_order.Column(db_order.Integer)
    last = db_order.Column(db_order.Integer) #если 1 - не обрабатываем

    def __repr__(self):
        return '<Order %r>' % self.id

db_order.create_all()

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/account/<token>")
def about(token):
    if token in online_users:
        return render_template('managet_account.html', login=online_users[token][0])
    return 'Ошибка доступа'
    

@app.route('/')
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
        return redirect("/home")

@app.route('/del') 
def delete(): 
    database = Order.query.all() 
    for i in range(1, len(database) + 1): 
        data = Order.query.get(1)

        db_order.session.delete(data) 
        db_order.session.commit() 
    return {'success': True}

def get_place_from_database():
    database = Order.query.all()
    for i in range(1, len(database) + 1):
        data = Order.query.get(i)
        print(i, data.place, sep=': ')

@app.route('/all_orders') 
def orders(): 
    get_place_from_database()

    database = Order.query.all()

    return render_template('all_orders.html', data=database)

@app.route('/do_order', methods=['POST'])
def he1o():
    full_name = request.headers['Fio'] 
    email = request.headers['Email'] 
    phone_number = request.headers['Number'] 
    place = " ".join(str(x) for x in request.headers['Place'].split(","))
    time = request.headers['Time']

    print(full_name, email, phone_number, place, time, sep='\n')

    new_order = Order(full_name=full_name, email=email, phone_number=phone_number, place=place, time=time, manager=-1, last=0)
    db_order.session.add(new_order)
    db_order.session.commit()

    return {'success': True}

if __name__ == "__main__":
    app.run(debug=True)