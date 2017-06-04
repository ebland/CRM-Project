import os
import json
import datetime
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
from model import connect_to_db, db, Job, Product, User, Role_ID, Job_Product, Product


app = Flask(__name__)

app.secret_key = "ABC"

#@app.errorhandler(404)
#def page_not_found(error):

    #return render_template('page_not_found.html'), 404


@app.route('/homepage')
def index():
    """Homepage."""

    return render_template("homepage.html")


# @app.route('/search')
# def search(): 
#    """"Search Site with Keyword in SideBar."""

#     return render_template('search_result_form.html')


@app.route('/search_process', methods=['POST'])
def search_process():
    #return 'a search'
     # 1. set email and password from form 
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    #return fname

    try:
        customer = User.query.filter_by(fname=fname).first()
        first_name = customer.fname
        last_name = customer.lname
        #customer = db.session.query(Customer).filter(Customer.fname==fname).filter(Customer.lname==lname).one()
    except:
        return "Customer not found!!! "
        flash("Customer not found!!!")
        return render_template('login_form.html')
     
    return render_template("/", first_name=first_name, last_name=last_name )


@app.route('/login')
def login():
    """Logs in a user"""

    return render_template('login_form.html')
 

@app.route('/login_process', methods=['POST'])
def login_process():
    """Logs in a user"""
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:  
    
        flash('User not found!')
        return render_template("homepage.html")
    elif email == str(user.email):
     
        session['user_id'] = user.user_id
        session['role_ids'] = []

    for role in user.roles:
        session['role_ids'].append(role.role_id)
    flash('User: {} has been logged in!'.format(email) )

    if  3 in session['role_ids']:
        user = User.query.filter_by(email=email).first()
        jobs = Job.query.filter_by(customer_id=user.user_id).all()  
        return render_template('homepage.html', current_user=user, jobs=jobs)      
    
    if  1 in session['role_ids']:
        user = User.query.filter_by(email=email).first()
        jobs = Job.query.filter_by(customer_id=user.user_id).all()
        users = User.query.filter_by(email=email).all()
        productcount = Product.query.count()
        customerjobcount = Job.query.filter(Job.customer_id == user.user_id).count()
        usercount = User.query.count()
        jobcount = Job.query.count()
        invoicecount = Job.query.filter_by(status='invoice_sent').count()
        return render_template('homepage.html', current_user=user, 
                               usercount=usercount, jobcount=jobcount,
                               productcount=productcount,
                               invoicecount=invoicecount)

    if  2 in session['role_ids']:
        user = User.query.filter_by(email=email).first()
        jobs = Job.query.filter_by(customer_id=user.user_id).all()
        return render_template('homepage.html', current_user=user)       
    
    return render_template('login_form.html')


@app.route('/logout')
def logout():
    """Logs a user out"""

    if (session['user_id'] != None):
        if session['user_id'] == True:
            del session['user_id']
            flash('User has been logged out')
            return render_template('homepage.html')
    else:
        return render_template('homepage.html')

@app.route('/delete_user')
def delete_user():
    """Deletes a user"""
    return render_template('delete_user_form.html')

@app.route('/show_user/<int:user_id>')
def show_user(user_id):
    """Shows Detailed information of Chosen User"""

    user = User.query.filter_by(user_id=user_id).first()

    return render_template('show_user.html', user=user)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show User Information"""
   
    user = User.query.filter_by(user_id=user_id).first()
    
    return render_template('customer_profile.html', user=user)


@app.route('/all_users')
def user_list():
    """Show List of All Users in ECRM."""
    
    users = User.query.all()

    return render_template("all_users.html", users=users)


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
  
        user = User(fname=fname, lname=lname, zip_code=zip_code, email=email, created_at=created_date, password=password, phone=phone, phone2=phone2, address1=address1, address2=address2, city=city, state=state)

        db.session.add(user)
   
        db.session.commit()
  
        flash("User was addded successfully!!!")
        
        return redirect('/homepage')

    else:
        return render_template('create_new_user.html')


@app.route('/update_user',  methods=[ "POST"])
def update_user():

    user_id = request.form.get('id')
    email = request.form.get('email')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    #return user_lname
    
    #get user you clicked on and passed user_id in URL
    user = User.query.filter(user_id == user_id,email == email, fname==fname, lname==lname  ).first()


    return render_template('update_user.html', user=user)


@app.route('/update_user_process', methods=['POST'])
def update_user_process():
    """Update Existing User."""

    page = 'update_user_process'

    if request.method == "POST":
        user_id = request.form.get('user_id')
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

        #get user you clicked on and passed user_id in URL
        user = User.query.filter(user_id == user_id,email == email ).first()

        #reset found user record with form posted values
        user.fname=fname
        user.lname=lname
        user.zip_code=zip_code
        user.email=email
        user.created_at=created_date
        user.password=password
        user.phone=phone
        user.phone2=phone2
        user.address1=address1
        user.address2=address2
        user.city=city
        user.state=state
        # update db record
        db.session.add(user)
        db.session.commit()

        flash("User was updated successfully!!!")
        user = User.query.filter(user_id == user_id,email == email )
        users = User.query.all()

        return render_template("all_users.html", users=users)

@app.route('/all_staff')
def all_staff():
    """Show List of All Staff in ECRM."""
    #TOOOO   TO DO TO DO DOOO6/2/17 QUEARY ONLY ROLE_ID 1 AND 3 AS STAFF
    staff = User.query.all()

    return render_template("all_staff.html", staff=staff)


@app.route('/all_jobs')
def job_list():
    """Show List of All Jobs in ECRM."""
    
    jobs = Job.query.all()

    return render_template("all_jobs.html", jobs=jobs)


@app.route('/all_job_table')
def job_table():
    """Show List of All Jobs in ECRM."""
    
    jobs = Job.query.all()

    return render_template("all_job_table.html", jobs=jobs)


@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    """Show Job Information"""
   
    job = Job.query.filter_by(job_id=job_id).first()

    return render_template('job_detail.html', job=job)   


@app.route('/job_form')
def job_form():
    """Create Job"""
    
    roles = Role_ID.query.all()
    users = User.query.all()

    staff_list =[]
    customer_list = []

    for user in users:
        if Role_ID.query.get(2) in user.roles:
            staff_list.append(user)
        if Role_ID.query.get(3) in user.roles:
            customer_list.append(user)    

    return render_template('job_form.html', roles=roles, staff_list=staff_list,
                           customer_list=customer_list)  


@app.route('/job_update_process', methods=['POST'])
def update_job():

    job_id = request.form.get('job_id')
    name = request.form.get('name')
    #return str(name)
 
    if job_id is not None:
        job_id = int(job_id)
    
    job = Job.query.filter(job_id==job_id).first()
    #return str(job.job_id)
    #reset record to form job name
    job.name = str(name)

     
    # update db record
    db.session.add(job)
    db.session.commit()

    jobs = Job.query.all()

    return render_template("all_jobs.html", jobs=jobs)



@app.route('/job_delete/<int:job_id>', methods=["GET"])
def job_delete(job_id):

    # job_to_delete = 0
    # job_to_delete = request.form.get('job_id')
    # if job_to_delete is not None and code.isnumeric():
    #     job_t_delete = int(job_to_delete)

    #invoice = Invoice.query.filter(Invoice_number==invoice_id).first()
    job = Job.query.filter_by(job_id=job_id).first()  #job_id==invoice_id
    #return str(job.job_id)

    #session.query(MenuItem).filter_by(id=menu_id)
    db.session.delete(job)
    db.session.commit()

    #flash(gettext(u"Delete Succesfully!"))

    jobs = Job.query.filter().all()   

    return render_template("all_jobs.html", jobs=jobs)


@app.route('/create_job_process', methods=['POST'])
def create_new_job(job_id):
    """Create New Job."""

    job_id = request.form.get('job_id')
    name = request.form.get('name')
    description = request.form.get('description')
    user_id = request.form.get('user_id')
    customer_id = request.form.get('customer_id')
    job_location = request.form.get('job_location')
    total = request.form.get('total')

    job = Job(job_id=job_id, name=name, description=description, 
                      user_id=user_id, customer_id =customer_id, 
                      job_location=job_location, total=total)

    db.session.add(job)
    db.session.commit()

    flash("Job added successfully!!!")
        
    return redirect('/all_jobs')


@app.route('/all_products')
def product_list():
    """Show List of All Products in ECRM."""
    
    products = Product.query.all()

    return render_template("all_products.html", products=products)


@app.route('/product_form')
def product_form():
    """Create Job"""
    #return "1"
    roles = Role_ID.query.all()
    users = User.query.all()

    staff_list =[]
    customer_list = []

    for user in users:
        if Role_ID.query.get(2) in user.roles:
            staff_list.append(user)
        if Role_ID.query.get(3) in user.roles:
            customer_list.append(user)    

    return render_template('product_form.html', roles=roles, staff_list=staff_list,
                           customer_list=customer_list)  


@app.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    """Show Product Information"""
   
    product = Product.query.filter_by(product_id=product_id).first()
    
    return render_template('product_detail.html', product=product)   


@app.route('/new_product_form')
def create_product_form():
    """Show product form."""
    
    return render_template('product_form.html') 


@app.route('/products/<int:product_id>')
def products(product_id):
    """Show Product Information"""
   
    product = Product.query.filter_by(product_id=product_id).first()

    return render_template('product_detail.html', product=product)   


@app.route('/create_product_process', methods=['POST'])
def create_new_product():
    """Create or ADD Product."""

    product_name = request.form.get('name')
    description = request.form.get('description')
    product_number = request.form.get('product_number')
    product_type = request.form.get('product_type')
    created_date = datetime.datetime.now()
    price = request.form.get('price')

    product = Product(product_name=product_name, description=description, 
                      product_number=product_number, 
                      product_type=product_type, 
                      created_at=created_date, price=price)

    db.session.add(product)
    db.session.commit()

    flash("Product added successfully!!!")

    products = Product.query.all()

    return render_template("all_products.html", products=products)
  
 
@app.route('/product_update_process', methods=['POST'])
def update_product():

    product_id = request.form.get('product_id')
    name = request.form.get('name')
    description = request.form.get('description')
    product_number = request.form.get('description')
    
 
    if product_id is not None:
        product_id = int(product_id)
    
    product = Product.query.filter(product_id==product_id).first()
    product.product_name  = str(name)
    product.description = str(description)
    product.description = product_number
     

    db.session.add(product)
    db.session.commit()

    products = Product.query.all()

    return render_template("all_products.html", products=products)


@app.route('/product_delete/<int:product_id>', methods=["GET"])
def product_delete(product_id):

    product = Product.query.filter_by(product_id=product_id).first()  
  
    db.session.delete(product)
    db.session.commit()

    products = Product.query.filter().all()   

    return render_template("all_products.html", products=products)


@app.route('/invoice_detail/<int:job_id>')
def invoice_detail(job_id):
    """Show User Information"""
   
    job = Job.query.filter_by(job_id=job_id).first()
    
    return render_template('job_detail.html', job=job)   


@app.route('/all_invoices')
def invoice_list():
    """Show List of All Invoices in ECRM."""
    return "1"

    job = job.query.filter_by(status='invoice_sent').all()

    return render_template("all_invoices.html", invoices=invoices)


@app.route('/invoice_form')
def invoice_form():
    """Invoice form for new entries in ECRM."""

    invoices = Invoice.query.all() 

    return render_template("invoice_form.html", invoices=invoices)

 
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

    return redirect(url_for('homepage')) 
    
    return render_template('create_new_user.html', page=page)


@app.route('/invoice/confirm/<int:invoice_id>')
def confirm_invoice(invoice_id):
   
    invoice = Invoice.query.filter(Invoice.id==invoice_id).first()
    invoice.confirm = datetime.datetime.now()

    db.session.commit()

    return redirect(url_for('show_invoice', invoice_id=invoice.id))


@app.route('/invoice/paid/<int:invoice_id>')
def invoice_paid(invoice_id):
    
    invoice = Invoice.query.filter(invoice_number==invoice_id).first()
    invoice_paid = datetime.datetime.now()

    db.session.commit()

    return redirect(url_for('show_invoice', invoice_id=invoice_number))


@app.route('/invoice/delete/<int:invoice_id>')
def invoice_delete(invoice_id):
   
    invoice_id = request.form.get('invoice_id')
    #job_id==invoice_id
    invoice = Job.query.filter().first()
    # invoice = Invoice.query.filter(Invoice_number==invoice_id).first()
    # job_id==invoice_id
    invoices = Job.query.filter().all()
    # db.session.delete(invoice) ???? KEEP
    # db.session.commit() #?????? KEEP
    flash(gettext(u"Delete Succesfully!"))
    return redirect(url_for('all_invoices'))

    db.session.delete(invoice)
    db.session.commit()

    return render_template("all_invoices.html", invoices=invoices)


@app.route('/invoice_update/<int:invoice_id>', methods=["GET"])
def invoice_update(invoice_id):

    invoice_id = request.form.get('invoice_id')

    invoice = User.query.filter_by(lname='Leslie').first()

    invoice.name = 'Leslie'
    db.session.commit()



    #invoice = Job.query.filter().first()  #job_id==invoice_id

    #invoices = Job.query.filter().first().update({"job_name": u"Bob Marley"})
    #invoices = session.query(Job).filter_by(job_id==invoice_id).first()
    #invoices = Job.query.filter().all()  #job_id==invoice_id
    #return render_template("all_invoices.html", invoices=invoices)

    #if request.method == "GET" :
    #invoice_id = request.form.get('invoice_id')
    #fname = request.form.get('fname')
    #lname = request.form.get('lname')


    #invoice = User(fname=fname, lname=lname, zip_code=zip_code, email=email, created_at=created_date, password=password, phone=phone, phone2=phone2, address1=address1, address2=address2, city=city, state=state)


    #flash(gettext(u"Update Succesfully!"))
    invoices = Job.query.filter().all()  #job_id==invoice_id
    return render_template("all_invoices.html", invoices=invoices)

# @app.route('/all_invoices/', methods=['POST'])

#TO DO:// get this working to post to html with tite create_invoice.html
@app.route('/create_new_invoice/', methods=["GET", "POST"])
def new_invoice():
    
    invoice_id=()
    page = 'create_new_invoice'

 #TO DO:// LINK ALL TOGETHER
@app.route('/create_invoice_form')
def create_invoice_form():

    page = 'create_invoice'
    return render_template('create_new_invoice.html', page=page)

    name = request.form.get('name')
    description = request.form.get('description')
    job_id = request.form.get('job_id')
    invoice_created_date = datetime.datetime.now()
    #invoice_due_date = datetime.datetime()
    phone = request.form.get('phone')
    location_address1 = request.form.get('location_address1')
    location_address2= request.form.get('location_address2')
    location_city = request.form.get('city')
    location_state = request.form.get('state')
    company = request.form.get('company')
    date_paid = request.form.get('date_paid')
    date_sent = request.form.get('date_sent')
   
    invoice = Invoice(name=name, description=description,job_id=job_id, 
                    location_address1=location_address1, location_address2=location_address2, location_city=location_city, location_state=location_state)
   
    db.session.add(invoice)
   
    db.session.commit()
    
    flash("Invoice created successfully!!!")

    return redirect(url_for('create_invoice', create_invoice=create_invoice)) 
    
    return render_template('invoice_form.html', page=page)


@app.route('/create_invoice_process', methods = ['GET', 'POST'])
def create_invoice_process():
    task = raw_input("Enter 'n' to create new invoice, press 'q' to exit: ")

    product_number = request.form.get('product_number')
    product_quantity = request.form.get('product_quantity')
    product_price = request.form.get('product_price')

    product_number = "product_number"
    product_quantity = "product_quantity"
    product_price = "product_price"

    product_total = int(product_price) * int(product_quantity)

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
                        price = int(float(single_product[2]))
                        total = int(float((price) * int(quantity)))
                        # price = float(single_product[2])
                        # total = float((price) * int(quantity))
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

    return render_template("invoice_form.html")


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['data_file'].read().decode('utf-8')

    # - debugging
    # file_contents = codecs.open(file_contents, "r", encoding='utf-8', errors='ignore')
    # f = codecs.open(request.files['data_file'], "r", encoding='utf-8', errors='ignore')
    # f = codecs.decode(request.files['data_file'], 'utf-8', 'ignore')
    if not f:
        flash("Error. File upload attempt detected, but no file found. Please contact the application administrator.",
              'danger')

    # To do: Get the conditional below to work, and remove the placeholder 'if True'.
    # if type(f) == '.csv':
    if True:
        f = csv2json_conversion(f)
        import_data = Import_Data(f)
        data_context = request.form['form_submit']
        valid_schema = validate_columns(import_data, data_context)
        if valid_schema == True:
            validated_data = validate_import(current_user, import_data, data_context)
            if validated_data:
                add_to_db(validated_data, data_context)
    else:
        flash('Error. Incorrect file type. The only file types accepted are: .csv', 'danger')

    return redirect(request.referrer)

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(port=5001, host='0.0.0.0')

