
import json
import datetime
import os
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from model import connect_to_db, db, Customer, Invoice, Product, Invoice_Detail, Role_ID, User 

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/search')
def search():
    """Search."""

    fname = request.args.get('fname')
    lname = request.args.get('lname')

    try:
        customer = db.session.query(Customer).filter(Customer.fname==fname).filter(Customer.lname==lname).one()
    except:
        flash("Customer not found!!!")
        return redirect('/')

    return render_template("search_results.html", customer=customer)


@app.route('/login', methods=['POST'])
def login():
    """Logs in a user"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found!')
    elif password == str(user.password):
        session['user_id'] = user.user_id
        flash('User: {} has been logged in!'.format(email))
        return redirect('/dashboard')
    else:
        flash('Password does not match!')

    return render_template('login_form.html')


@app.route('/logout')
def logout():
    """Logs a user out"""

    del session['user_id']
    flash('User has been logged out')

    return render_template('homepage.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard"""
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    role = user.roles.name
    # if the role is admin
    #   find show quotes, customers, jobs
    #   show admin dashboard, passing in data
    # if the role is customer
    #   find quotes, projects, invoices
    #   show the customer dash, pass in data
    # ... same for estimator, staff


#     return render_template('templates/dashboard.html', page=page)


@app.route('/add_customer')
def add_customer():
    """Display Add Customer Form"""
    
    return render_template("templates/create_new_user.html")


@app.route('/process_add_customer')
def add_customer_to_db():
    """Add customer to DB."""
    f_name = request.args.get('fname')
    l_name = request.args.get('lname')
    zip_code = request.args.get('zipcode')
    email = request.args.get('email')
    created_date = datetime.datetime.strptime(
            str(request.get['datetime']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
    password = request.args.get('password')
    phone = request.args.get('phone')
    phone2 = request.args.get('phone2')
    address1 = request.args.get('address1')
    address12= request.args.get('address2')
    city = request.args.get('city')
    state = request.args.get('state')
  

    customer = Customer(fname=f_name, lname=l_name, zipcode=zip_code, email=email,
                        password=password, phone=phone, phone2=phone2, 
                        address1=address1, address2=address2, city=city, state=state)
   
    db.session.add(customer)
   
    db.session.commit()
    
    flash("Customer was addded successfully!!!")

    return redirect(url_for('/')) #DASHBOARD??????

    else:
        return render_template('templates/create_new_user.html', page=page)

@app.route('/create_new_user/', methods=["GET", "POST"])
def new_user():
    page = 'All Users'
    if request.method == "POST":
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        f_name = request.args.get('fname')
        zip_code = request.args.get('zipcode')
        email = request.args.get('email')
        created_date = datetime.datetime.strptime(
            str(request.get['datetime']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        password = request.args.get('password')
        phone = request.args.get('phone')
        phone2 = request.args.get('phone2')
        address1 = request.args.get('address1')
        address12= request.args.get('address2')
        city = request.args.get('city')
        state = request.args.get('state')
        #IF STAFF add these two ASK LESLIE HOW ORGANIZE
        # job_title = request.form['job_title']
        # department = request.form['department']
  
        user = User(fname=f_name, lname=l_name, zipcode=zip_code, email=email, created_date=datetime,
                        password=password, phone=phone, phone2=phone2, 
                        address1=address1, address2=address2, city=city, state=state)

        db.session.add(user)
   
        db.session.commit()
  
        flash("User was addded successfully!!!")
        
        return redirect(url_for('/'))

    else:
        return render_template('templates/create_new_user.html', page=page)


#to display all quotes in system NEED TO DECIDE HOW TO ORGANIZE
# @app.route('/templates/quotes/invoices?/TBD', methods=['POST'])


# @app.route('invoices/new_quote/', methods=['POST'])

# def new_quote():
#     quote_number = request.form['quote_number']
#     #I want to do a timestamp here UNIX
#     # customer_id
#     #user_id
#     # product_number
#     # status
#     # in_stock
#     # in_stock_date
#     created_date = (request.form['date_received']),

#to display all invoices in system
# @app.route('/all_invoices/', methods=['POST'])


# @app.route('/create_invoice/', methods=["GET", "POST"])
# # def new_invoice():
# #     invoice_number = request.form['invoice_number']
# #     #I want to do a timestamp here UNIX
# #     # product_number
# #     # purchase_order_number
# #     # status
# #     # in_stock
# #     # in_stock_date
# #     created_date = (request.form['date_received']),



if __name__ == "__main__":
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug  

    connect_to_db(app)

    # # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(port=5001, host='0.0.0.0')

# if __name__ == '__main__':
#     app.run(app, host='0.0.0.0', debug=True)