import simplejson
import json
import datetime
import os
from jinja2 import StrictUndefined
app.jinja_env.undefined = StrictUndefined
from flask import Flask, jsonify, render_template, request, flash,
    redirect, url_for,
from model import connect_to_db, db, Customer, Invoice, Product, 
    InvoiceDetail, Role, User, Client, 

app = Flask(__name__)

app.secret_key = "ABC"

# ??from flask_debugtoolbar import DebugToolbarExtension
# ??user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# Ask Leslie if the LoginManager found during research & WTF Forms  
#  add on for Jinja would be ok to incorporate into my project.


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/search')
def search():
    """Search."""
    # import pdb; pdb.set_trace()
    # 1. get form inputs (fname, lname)
    fname = request.args.get('fname')
    lname = request.args.get('lname')

    # 2. Search DB using SQLAlchemy for fname and lname (Table name is customerts)
    try:
        customer = db.session.query(Customer).filter(Customer.fname==fname).filter(Customer.lname==lname).one()
    except:
        flash("Customer not found!!!")
        return redirect('/')

    # 3. Display search results
    return render_template("search_results.html", customer=customer)

# Notes TO Refer Back to Regarding APPS from Ahmed
# @app.route('/add-customer')
# def add_customer():
#     """Display Add Customer Form"""
    
#     return render_template("add_customer.html")

# @app.route('/process_adding_customer')
# def add_customer_to_db():
#     """Add customer to DB."""
#     f_name = request.args.get('fname')
#     l_name = request.args.get('lname')
#     zip_code = request.args.get('zipcode')

#     # To add this customer to db:
#     # 1. Create the customer
#     customer = Customer(fname=f_name, lname=l_name, zipcode=zip_code)

#     # 2. Add this customer to session
#     db.session.add(customer)

#     # 3. Commit the changes
#     db.session.commit()

#     # 4. Display a flash message to confirm adding
#     flash("Customer was addded successfully!!!")

#     return redirect("/")

# from .models import User, Customers, Personnel, Messages, Result, AppNotifications, OmsConfig


# class Customer(db.Model):
#     """Customers table"""

#     __tablename__ = "customers"

#     id = db.Column(db.Integer,
#                        primary_key=True,
#                        autoincrement=True)
#     fname = db.Column(db.String(50), nullable=False)
#     lname = db.Column(db.String(50), nullable=False)
#     zipcode = db.Column(db.String(50), nullable=False)


# from jinja2 import StrictUndefined

# from flask import Flask, jsonify, render_template, request, flash, redirect
# from flask_debugtoolbar import DebugToolbarExtension

# from model import connect_to_db, db, Customer


# app = Flask(__name__)

# # Required to use Flask sessions and the debug toolbar
# app.secret_key = "ABC"

# app.jinja_env.undefined = StrictUndefined


# @app.route('/')
# def index():
#     """Homepage."""
#     return render_template("homepage.html")

# @app.route('/search')
# def search():
#     """Search."""
#     # import pdb; pdb.set_trace()
#     # 1. get form inputs (fname, lname)
#     fname = request.args.get('fname')
#     lname = request.args.get('lname')

#     # 2. Search DB using SQLAlchemy for fname and lname (Table name is customerts)
#     try:
#         customer = db.session.query(Customer).filter(Customer.fname==fname).filter(Customer.lname==lname).one()
#     except:
#         flash("Customer not found!!!")
#         return redirect('/')

#     # 3. Display search results
#     return render_template("search_results.html", customer=customer)


# @app.route('/add-customer')
# def add_customer():
#     """Display Add Customer Form"""
    
#     return render_template("add_customer.html")

# @app.route('/process_adding_customer')
# def add_customer_to_db():
#     """Add customer to DB."""
#     f_name = request.args.get('fname')
#     l_name = request.args.get('lname')
#     zip_code = request.args.get('zipcode')

#     # To add this customer to db:
#     # 1. Create the customer
#     customer = Customer(fname=f_name, lname=l_name, zipcode=zip_code)

#     # 2. Add this customer to session
#     db.session.add(customer)

#     # 3. Commit the changes
#     db.session.commit()

#     # 4. Display a flash message to confirm adding
#     flash("Customer was addded successfully!!!")

#     return redirect("/")


@app.route('/add-customer')
def add_customer():
    """Display Add Customer Form"""
    
    return render_template("add_customer.html")

@app.route('/process_adding_customer')
def add_customer_to_db():
    """Add customer to DB."""
    f_name = request.args.get('fname')
    l_name = request.args.get('lname')
    zip_code = request.args.get('zipcode')

    # To add this customer to db:
    # 1. Create the customer
    customer = Customer(fname=f_name, lname=l_name, zipcode=zip_code)

    # 2. Add this customer to session
    db.session.add(customer)

    # 3. Commit the changes
    db.session.commit()

    # 4. Display a flash message to confirm adding
    flash("Customer was addded successfully!!!")

@app.route('/add_customer')   
def new_user():
    """process_adding_customer"""
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        created_date = datetime.datetime.strptime(
            str(request.form['start_date']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        email = request.form['email']
        password = encrypt_password('Hackbr1ght')
        if (User.query.filter_by(email=email)).count() > 0:
            flash('User already exists, try again or login.', 'alert-danger')
            return render_template(
                'templates/new_user.html',
                page=page
            )
        else:
            user_datastore.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                start_date=start_date,
            )
            db.session.commit()
            flash('New user created successfully', 'alert-success')
            return redirect(url_for('/'))

    else:
        return render_template('templates/new_user.html', page=page)
    return redirect("/")

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
        # return render_template('homepage.html')
        return redirect('homepage.html/'+str(user.user_id))

    else:
        flash('Password does not match!')

    return render_template('login_form.html')


@app.route('/logout')
def logout():
    """Logs a user out"""

    del session['user_id']
    flash('User has been logged out')

    return render_template('homepage.html')


@app.route('new_user/', methods=["GET", "POST"])
#???Ask Leslie how to connect this "@login_required" to result of route above
#???Ask Leslie how to connect this "@role_id_required('admin')to check user role
def new_user():
    page = 'All Users'
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = datetime.datetime.strptime(
            str(request.form['start_date']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        email = request.form['email']
        job_title = request.form['job_title']
        department = request.form['department']
        password = encrypt_password('Hackbr1ght')
        if (User.query.filter_by(email=email)).count() > 0:
            flash('User already exists, try again or login.', 'alert-danger')
            return render_template(
                'templates/new_user.html',
                page=page
            )
        else:
            user_datastore.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                start_date=start_date,
                job_title=job_title,
                department=department
            )
            db.session.commit()
            flash('New user created successfully', 'alert-success')
            return redirect(url_for('/'))

    else:
        return render_template('templates/new_user.html', page=page)




@app.route('/')
#???Ask Leslie how to connect this "@login_required" to result of route above
#???Ask Leslie how to connect this "@role_id_required('admin')to check user role
def dashboard():
    page = "Dashboard"
    return render_template('templates/dashboard.html', page=page)




@app.route('new_user/', methods=["GET", "POST"])
#???Ask Leslie how to connect this "@login_required" to result of route above
#???Ask Leslie how to connect this "@role_id_required('admin')to check user role
def new_user():
    page = 'All Users'
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = datetime.datetime.strptime(
            str(request.form['start_date']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        email = request.form['email']
        job_title = request.form['job_title']
        department = request.form['department']
        password = encrypt_password('Hackbr1ght')
        if (User.query.filter_by(email=email)).count() > 0:
            flash('Email existed, please choose another one', 'alert-danger')
            return render_template(
                'templates/new_user.html',
                page=page
            )
        else:
            user_datastore.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                start_date=start_date,
                job_title=job_title,
                department=department,
            )
            db.session.commit()
            flash('New account created', 'alert-success')
            return redirect(url_for('/'))

    else:
        return render_template('new_user.html', page=page)


@app.route('/templates/admin/user_profiles<path:user_id>/view/', methods=["GET", "POST"])
#???Ask Leslie how to connect this "@login_required" to result of route above
#???Ask Leslie how to connect this "@role_id_required('admin')to check user role
def user_profiles(user_id):
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = datetime.datetime.strptime(
            str(request.form['start_date']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        # email = request.form['email']
        job_title = request.form['job_title']
        department = request.form['department']
        role = Role.query.filter_by(id=request.form['role']).first()
        password = request.form['password']

        if User.query.filter_by(id=user_id).count() == 1:
            user = User.query.filter_by(id=user_id).first()
            if role is not None:
                user.roles = []
                user.roles.append(role)
            user.first_name = first_name
            user.last_name = last_name
            user.start_date = start_date
            user.job_title = job_title
            user.department = department
            if password:
                user.password = encrypt_password(password)
            db.session.commit()
            flash('Account updated', 'alert-success')
            return redirect(url_for('/'))

        else:
            flash('Email existed, please choose another one', 'alert-danger')
            return render_template(
                'templates/admin/new_user.html',
                page=page
            )
    else:
        user = User.query.filter_by(id=user_id).first()
        roles = Role.query.all()
        return render_template(
            '/templates/admin/user_profiles.html',
            page=page,
            user=user,
            roles=roles
        )


@app.route('/templates/TBD?invoices/', methods=['POST'])
#???Ask Leslie how to connect this "@login_required" to result of route above
#???Ask Leslie how to connect this "@role_id_required('admin')
#@roles_accepted('admin', 'etc..') to check user role_id


@app.route('invoices/new_invoice/', methods=['POST'])
#???Ask Leslie how to connect this "@login_required" to result of route above
#???Ask Leslie how to connect this "@role_id_required('admin')
#@roles_accepted('admin', 'etc..') to check user role_id
def new_invoice():
    invoice_number = request.form['invoice_number']
    #I want to do a timestamp here UNIX
    received_date = us_to_sql_date(request.form['date_received']),
    product_numbers = filter(None, request.form.getlist('product_numbers[]'))
    product_numbers = [x.upper() for x in product_numbers]
    if Invoice.query.get(invoice_number):
        flash("Invoice number already exists", 'alert-danger')
        return redirect(url_for('new_invoice'))
    invoice = Invoice(
        invoice_number=invoice_number,
        received_date=received_date
    )
        product = product.get_or_create(x, db.session)
        invoice_detail.product = product
        invoice.products.append(invoice_detail)
    db.session.add(invoice)
    db.session.commit()
    flash('Invoice created successfully', 'alert-success')
    return redirect(url_for('invoices'))



if __name__ == "__main__":
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug  

    connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5001, host='0.0.0.0')

# if __name__ == '__main__':
#     app.run(app, host='0.0.0.0', debug=True)