from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/nohunger'  # Update with your DB details
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Fooditem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phn = db.Column(db.String(100))
    foodtype = db.Column(db.String(200))
    date= db.Column(db.String(200))
    expire_time = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    location= db.Column(db.String(200))
    description = db.Column(db.String(200))



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phn = db.Column(db.String(100))
    foodtype = db.Column(db.String(200))
    date= db.Column(db.String(200))
    expire_time = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    location= db.Column(db.String(200))
    description = db.Column(db.String(200))
    
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/map')
def map():
    return render_template('map.html')



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and user.password==password:
            flash('Login Success','success')
            return render_template('login.html')
        else:
            flash('Invalid credentials','danger')
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    
    return render_template('thankyou.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == "POST":
        name = request.form['name']
        phn=request.form['phn']
        description = request.form['description']
        quantity = request.form['quantity']
        type=request.form['foodtype']
        date=request.form['date']
        expire=request.form['expire_time']
        location=request.form['location']
         
        item = Fooditem(name=name,phn=phn,foodtype=type,date=date,expire_time=expire,quantity=quantity,location=location,description=description)
        db.session.add(item)
        db.session.commit()
       
        flash('Food donation successful', 'success')
       
        return render_template('thankyou.html')
    return render_template('donate.html')

@app.route('/logout')
def logout():
    return render_template('home.html')


@app.route('/getfood', methods=['GET', 'POST'])
def getfood():
    food=Fooditem.query.all()
    return render_template('getfood.html',food=food)
    
    

@app.route('/cart/<string:id>', methods=['GET', 'POST'])
def cart(id):
    flash('Food ordered', 'success')
    cart = Fooditem.query.filter_by(id=id).first()
    db.session.delete(cart)
    db.session.commit()
    food=Fooditem.query.all()
    return render_template('getfood.html',food=food)
@app.route('/newcart', methods=['GET', 'POST'])
def newcart():
    cart=Cart.query.all()
    return render_template('cart.html',cart=cart)
if __name__ == '__main__':
    app.run(debug=True)
