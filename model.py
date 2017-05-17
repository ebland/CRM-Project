from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()

class Customer(db.Model):
    """Customers table"""

    __tablename__ = "customers"

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    # Customer Information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_date = db.Column(db.DateTime())
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    def __init__(self, password, firstname, lastname, email, zipcode, phone, city, state):
        self.password=password
        self.fname = firstname
        self.lname = lastname
        self.email = email
        self.zip_code = zipcode
        self.phone = phone
        self.city = city
        self.state = state

def __repr__(self):
        return '<customers %r>' % (self.lname, self.fname)


class Role_ID(db.Model):
    """Role ID table."""

    __tablename__ ="roles"

    role_id = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User_Roles(db.Model):

    __tablename__="user_roles"

    user_role_id = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.role_id', ondelete='CASCADE'))


class User(db.Model):

    __tablename__ ="users"

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # Information
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50)) # if staff
    birth_date = db.Column(db.Date()) # if staff
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))

    # Account status
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    roles = db.relationship('Role_ID', secondary='user_roles') 
    roles = db.relationship('Role_ID', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    quotes = db.relationship('Quote', backref='user')
   
    def __init__(self, password, firstname, lastname, title, department, dob, email, zipcode, phone, city, state):
        self.password=password
        self.fname = firstname
        self.lname = lastname
        self.job_title = title
        self.department = department
        self.birth_date = dob
        self.email = email
        self.zip_code = zipcode
        self.phone = phone
        self.city = city
        self.state = state

def __repr__(self):
        return '<User %r>' % (self.lname, self.fname)

class Product(db.Model):

    __tablename__ ="product"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Unicode(50), nullable=False, primary_key=True, unique=True)
    product_number = db.Column(db.String(10))
    description = db.Column(db.Unicode(255))
    product_type = db.Column(db.Unicode(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.Unicode(500))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    
    quotes = db.relationship('quotes', backref=db.backref('product', lazy='joined'))
    invoices = db.relationship('invoice_Detail', back_populates='product')
    

class Quote(db.Model):

    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    product_quantity = db.Column(db.Integer)
    product_number = db.Column(db.Integer, db.ForeignKey('product.product_number'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    total = db.Column(db.Float(precision=10, decimal_return_scale=2, asdecimal=True))

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())

    users = db.relationship('User', backref=db.backref('user_id'))
    invoices = db.relationship('Invoice_Detail', back_populates='product')
    customer = db.relationship('Customer', backref=db.backref('quotes'))

class Invoice(db.Model):

    __tablename__ ="invoice"

    id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    desc = db.Column(db.String())
    invoice_number = db.Column(db.Unicode(50), primary_key=True, unique=True)
    invoice_created_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    invoice_due_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    
    product = db.relationship('invoice_Detail', back_populates="invoice")
    customers = db.relationship('Customer', backref=db.backref('invoice'))


class Invoice_Detail(db.Model):

    __tablename__ ="invoice_detail"

    id = db.Column(db.Integer, primary_key=True, unique=True)

    invoice_number = db.Column(db.Unicode(50), db.ForeignKey('invoice.invoice_number'))
    product_number = db.Column(db.Unicode(50), db.ForeignKey('product.product_number'))
    purchase_order_number = db.Column(db.Unicode(50))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    invoice = db.relationship('invoice', back_populates='products')
    product = db.relationship('product', back_populates='invoices')


#do I need to put this somewhere else to create the invoice total
app.jinja_env.globals.update(Create_Invoice=Create_Invoice)

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
        print '\single_product', quantity[i], product_list[i],' for the ' +
              'amount of $', product_price[i]
    print "Your total: $ ", sum(product_price)                    
    if (task == "q"):
        sys.exit()

            db.session.add(invoice)
            db.session.commit()
            return redirect(url_for('show_invoice'))

    return render_template("create_invoice.html", title = gettext('create_invoice'), form = form)

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
    invoice = Invoice.query.filter(Invoice_number==invoice_id).first()
    db.session.delete(invoice)
    db.session.commit()
    flash(gettext(u"Delete Succesfully!"))
    return redirect(url_for('all_invoices'))


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ecrm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


# make example data function
# create a customer - e.g. new_c = Customer(name = "Bob", ...)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."