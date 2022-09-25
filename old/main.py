import random, string
from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy

online_users = {}

MANAGERS = {"manager1": "123456", "manager2": "123456789", "manager3":  "123456",
"manager4":  "123456",
"manager5":  "123456",
"manager6":  "123456",
"manager7":  "123456",
"manager8":  "123456",
"manager9":  "123456",
"manager10":  "123456"}

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + '0123456789') for i in range(length))

def auth(l, p):
    if l == 'admin' and p == 'admin':
        return 2

    return MANAGERS[l] == p

    return 0

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
    type = db_order.Column(db_order.String(322))

    def __repr__(self):
        return '<Order %r>' % self.id

db_order.create_all()

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/account/<token>")
def about(token):
    if online_users[token][0] == 'admin':
        return render_template('admin.html')

    id_kenta = list(MANAGERS).index(online_users[token][0])

    __data__ = []

    database = Order.query.all() 
    for i in range(1, len(database) + 1): 
        data = Order.query.get(i)

        if data.manager == id_kenta and data.last == 0:
            __data__.append(data)

    if token in online_users:
        return render_template('managet_account.html', login=online_users[token][0], data=__data__)

    return 'Ошибка доступа'

@app.route('/')
def order():
    return render_template('order.html')

@app.route('/login', methods=['POST'])
def hello():
    login = request.form['login']
    password = request.form['password']

    global online_users

    sadf = auth(login, password)

    if sadf != 0:
        h = generate_random_string(64)
        online_users[h] = [login]
        return {'success': True, 'token': h}
    else:
        return redirect("/home")

@app.route('/del') 
def delete(): 
    '''data = Order.query.get(1)
    data.last = 0
    db_order.session.commit()''' 

    database = Order.query.all() 
    for i in range(1, len(database) + 1): 
        data = Order.query.get(i)

        if data.last == 0:
            data.last = 1

    db_order.session.commit()  

    return {'success': True}

def get_data_from_database():
    lst = []

    database = Order.query.all()
    for i in range(1, len(database) + 1):
        data = Order.query.get(i)

        if data.last == 0:
            lst.append([data.id, data.place, data.time])

    return lst

def get_data_from_db():
    database = Order.query.get(11)

    database.last = 1

    db_order.session.commit()

    database = Order.query.get(12)

    database.last = 1

    db_order.session.commit()

def edit(task_id, worker):
    database = Order.query.get(task_id)
    database.manager = worker

    db_order.session.commit()    

@app.route('/all_orders') 
def orders():
    #print(get_data_from_database())
    #edit(1, -1)

    database = Order.query.all()

    return render_template('all_orders.html', data=database)

@app.route('/do_order', methods=['POST'])
def he1o():
    full_name = request.headers['Fio'] 
    email = request.headers['Email'] 
    phone_number = request.headers['Number'] 
    place = " ".join(str(x) for x in request.headers['Place'].split(","))
    time = request.headers['Time']
    type_ = request.headers['Type']

    new_order = Order(full_name=full_name, email=email, phone_number=phone_number, place=place, time=time, manager=-1, last=0, type=type_)
    db_order.session.add(new_order)
    db_order.session.commit()

    #algorithm.init()
    return {'success': True}

if __name__ == "__main__":
    app.run(debug=True)