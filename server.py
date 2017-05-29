import os
import json
import datetime
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
from model import connect_to_db, db, Job, Product, User, Role_ID, Job_Product, Product, Invoice
from flask_debugtoolbar import DebugToolbarExtension
#from model import LoginManager, LoginForm
#app.jinja_env.undefined = StrictUndefined

app = Flask(__name__)

app.secret_key = "ABC"

#@app.errorhandler(404)
#def page_not_found(error):

    #return render_template('page_not_found.html'), 404

@app.route('/homepage')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/search')
def search():
    return 'a search'

    fname = request.args.get('fname')
    lname = request.args.get('lname')

    try:
        customer = db.session.query(Customer).filter(Customer.fname==fname).filter(Customer.lname==lname).one()
    except:
        flash("Customer not found!!!")
        return redirect('/')

    return render_template("search_results.html", user=user)


@app.route('/login')
def login():
    """Logs in a user"""
    return render_template('login_form.html')
 

@app.route('/login_process', methods=['POST'])
def login_process():
    """Logs in a user"""
    
    # 1. set email and password from form 
    email = request.form.get('email')
    password = request.form.get('password')

    # 2. call db and get matching record
    #user = User.query.filter_by(email='peter').first()
    #user = User.query.filter_by(email='ninja@hackbrightacademy.com').first()
    user = User.query.filter_by(email=email).first()
    print user
    # user.password = 1
    
    #3. handle use cases for record matched or not
    if not user:
        print "test"
        flash('User not found!')
        return redirect('/login')
    elif password == str(user.password):
        print "another test"
        session['user_id'] = user.user_id
        session['role_id'] = [] 
        for role in user.roles:
            session['role_ids'].append(role.name)

        flash('User: {} has been logged in!'.format(email))
        return redirect('/homepage')
    # else:
    #     flash('Password does not match!')

    return render_template('login_form.html')


@app.route('/logout')
def logout():
    """Logs a user out"""
    return 'a logout'

    # del session['user_id']
    flash('User has been logged out')
        
    return render_template('homepage.html')

@app.route('/show_user')
def show_user():
    """Shows Detailed information of Chosen User"""

    return render_template('show_user.html')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show User Information"""
   
    user = User.query.filter_by(user_id=user_id).first()
    
    return render_template('show_user.html', user=user)


@app.route('/dashboard')
def dashboard():
    """Dashboard"""

    return 'a dashboard'

    user_id = session.get('user_id')
    roles = session.get('role_id') 
    user = User.query.filter_by(user_id=user_id).first()

    if 'admin' in roles:
    #   show admin dashboard, passing in data
    #if the role is customer
    #   find quotes, projects, invoices
    #   show the customer dash, pass in data
    # ... same for estimator, staff
        return render_template('templates/dashboard.html', page=page)


@app.route('/all_users')
def user_list():
    """Show List of All Users is ECRM."""
    
    user = User.query.get(user_id)

    return render_template("templates/all_users.html", user=user)


@app.route('/create_new_user')
def create_new_user():
    """Creates a new user"""

    return render_template('create_new_user.html')


@app.route('/create_new_user_process', methods=["GET", "POST"])
def new_user():

    page = 'create_new_user'

    print(request.args.get('email'))
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        zip_code = request.form.get('zipcode')
        email = request.form.get('email')
        created_date = datetime.datetime.now()
        password = request.form.get('password')
        phone = request.form.get('phone')
        phone2 = request.form.get('phone2')
        address1 = request.form.get('address1')
        address2= request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
  
        user = User(fname=fname, lname=lname, zip_code=zip_code, email=email, created_at=created_date,
                        password=password, phone=phone, phone2=phone2, 
                        address1=address1, address2=address2, city=city, state=state)

        db.session.add(user)
   
        db.session.commit()
  
        flash("User was addded successfully!!!")
        
        return redirect('/homepage')

    else:
        return render_template('create_new_user.html')


@app.route('/process_add_customer', methods=["GET", "POST"])
def add_customer_to_db():
    """Add customer to DB."""
    
    page = 'create_new_user'
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    zip_code = request.form.gett('zipcode')
    email = request.form.get('email')
    created_at = datetime.datetime.now()
    password = request.form.get('password')
    phone = request.form.get('phone')
    phone2 = request.form.get('phone2')
    address1 = request.form.get('address1')
    address2= request.form.get('address2')
    city = request.form.get('city')
    state = request.form.get('state')
    company = request.form.get('company')
  
    customer = Customer(fname=fname, lname=lname, zipcode=zip_code, email=email,
                        password=password, phone=phone, phone2=phone2, 
                        address1=address1, address2=address2, city=city, state=state,
                        company=company)
   
    db.session.add(customer)
   
    db.session.commit()
    
    flash("Customer was addded successfully!!!")

    return redirect(url_for('/')) #DASHBOARD??????
    
    return render_template('create_new_user.html', page=page)


@app.route('/customers', methods=["POST"])
def show_customer():
    page='show_customer'
    if request.method == "POST":


        @app.route('/Create_Invoice/', methods = ['GET', 'POST'])
        def create_invoice():
            task = raw_input("Enter 'n' to create new invoice, press 'q' to exit: ")

        if (task == 'n'):
            product_list = []
            quantity = []
            product_price = []
    
    while True:
        product_number = raw_input("\nEnter the 8 digit item code. Or press 'q' " + 
                         "to quit: ")
        if (product_number == 'q'):
            print("\nQuitting ...\n")
            break
        if (len(product_number) != 8): 
            print("\nInvalid product number, please try again.")
        else:
            with open("product_list.txt") as products:
                for line in products:
                    if product_number in line:
                        single_product = line.split(" ")
                        quantity = input("\nQuantity of the product " +
                                         "to be purchased: ")
                        code = single_product[0]
                        product_name = single_product[1]
                        price = float(single_product[2])
                        total = (price) * int(quantity)
                        product_list.append(product_name)
                        quantity.append(quantity)
                        product_price.append(total)
                        break
    print ("Your invoice: ")
    for i in range(len(product_list)):
        print ('\single_product', quantity[i], product_list[i],' for the ' +
              'amount of $', product_price[i])
    print ("Your total: $ ", sum(product_price))                   
    if (task == "q"):
        sys.exit()

        db.session.add(invoice)
        db.session.commit()
        return redirect(url_for('show_invoice'))

    return render_template("create_invoice.html")

app.jinja_env.globals.update(Create_Invoice="create_invoice.html")

@app.route('/invoice/confirm/<int:invoice_id>')
def confirm_invoice(invoice_id):
    return 'a string'
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    invoice.confirm = datetime.datetime.now()
    db.session.commit()
    return redirect(url_for('show_invoice', invoice_id=invoice.id))


@app.route('/invoice/paid/<int:invoice_id>')
def invoice_paid(invoice_id):
    return 'a string'
    invoice = Invoice.query.filter(invoice_number==invoice_id).first()
    invoice_paid = datetime.datetime.now()
    db.session.commit()
    return redirect(url_for('show_invoice', invoice_id=invoice_number))


@app.route('/invoice/delete/<int:invoice_id>')
def invoice_delete(invoice_id):
    return 'a string'
    invoice = Invoice.query.filter(Invoice_number==invoice_id).first()
    db.session.delete(invoice)
    db.session.commit()
    flash(gettext(u"Delete Succesfully!"))
    return redirect(url_for('all_invoices'))



@app.route('/invoices/new_quote/', methods=['POST'])
def new_quote():
    quote_number = request.form['quote_number']
#     #I want to do a timestamp here UNIX
#     # customer_id
#     #user_id
#     # product_number
#     # status
#     # in_stock
#     # in_stock_date
#     created_date = (request.form['date_received']),

#invoice.get_status
#to display all invoices in system

# @app.route('/all_invoices/', methods=['POST'])


@app.route('/create_invoice/', methods=["GET", "POST"])
def new_invoice():
    invoice_number = request.form['invoice_number']
    invoice_id=()
# #     # product_number
# #     # purchase_order_number
# #     # status
# #     # in_stock
# #     # in_stock_date
# #     created_date = (request.form['date_received']),



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(port=5001, host='0.0.0.0')

