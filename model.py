from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
db = SQLAlchemy()


class User(db.Model):

    __tablename__="users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Information
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(50), nullable=True) 
    birth_date = db.Column(db.Date(), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    phone2 = db.Column(db.String(30), nullable=True)
    company = db.Column(db.String(40), nullable=True)
    # Address
    address1 = db.Column(db.String(255), nullable=True)
    address2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(20), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    module_abbreviation =db.Column(db.String(4), nullable=True)
    
    ######STATUS#######
    active = db.Column(db.Boolean())
    ######STATUS#######

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    roles = db.relationship('Role_ID', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User user_id=%d, email=%s>' % (self.user_id, self.email)


class Role_ID(db.Model):
    """Role ID table."""

    __tablename__="roles"

    role_id = db.Column(db.Integer, 
                      primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    ######STATUS#######
    active = db.Column(db.Boolean())
    ######STATUS#######


class User_Roles(db.Model):

    __tablename__="user_roles"

    user_role_id = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.role_id', ondelete='CASCADE'))



class Product(db.Model):
    """Products Table."""

    __tablename__="product"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_name = db.Column(db.Unicode(50), nullable=True)
    product_number = db.Column(db.String(10))
    description = db.Column(db.Unicode(255))
    product_type = db.Column(db.Unicode(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.Unicode(500))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    module_abbreviation =db.Column(db.String(4), nullable=True)
    jobs = db.relationship('Job', backref=db.backref('product', lazy='joined'), secondary='job_product')
    # , db.ForeignKey('invoice.product_number'), nullable=False, unique=True)
    

class Job_Product(db.Model):

    __tablename__="job_product"

    jpid = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id', ondelete='CASCADE'))
    job_id = db.Column(db.Integer(), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))


class Job(db.Model):

    __tablename__="jobs"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.ForeignKey('customer.customer_id'))
    # product_quantity=db.Column(db.Integer(2), nullable=False)
    module_abbreviation = db.Column(db.String(4), nullable=True)
    # quote_id = db.Column(db.Integer(11), db.ForeignKey('quotes.quote_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    total = db.Column(db.Float(precision=10, decimal_return_scale=2, asdecimal=True))
    product_id = db.Column(db.ForeignKey('product.product_id'))
    # c_total_net_amount = db.Column(db.Integer(5), db.ForeignKey(c_total_net_amount.c_total_net_amount(10,2)))
    # c_staff_total_amount = db.Column(db.Integer(5), db.ForeignKey(c_staff_total_amount.c_staff_total_amount(10,2)))
    # update_user_id = db.Column(db.Integer(11), nullable=True)
    # create_user_id = db.Column(db.Integer(11), nullable=False)

    ######STATUS#######
    active = db.Column(db.Boolean())
    status = db.Column(db.String(11))
    date_due = db.Column(db.DateTime())
    #####STATUS#####

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())

    user = db.relationship('User', backref=db.backref('user_jobs'), foreign_keys=[user_id])
    customer = db.relationship('User', backref=db.backref('customer_jobs'), foreign_keys=[customer_id])


# ----------------------

class Invoice(db.Model):

    __tablename__="invoice"

    invoice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id')) 
    user_id=db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    name = db.Column(db.String(90), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    module_abbreviation =db.Column(db.String(4), nullable=True)
    invoice_created_date = db.Column(db.DateTime())
    invoice_due_date = db.Column(db.DateTime)
    # customer_id = db.Column(db.Integer(11), db.ForeignKey('customer.customer_id'))
    job_id = db.Column(db.String(11))
    date_paid = db.Column(db.String(11))
    date_sent = db.Column(db.String(11))

    active = db.Column(db.String(11))
    # update_user_id = db.Column(db.Integer(11), nullable=True)
    # create_user_id=db.Column(db.Integer(11), nullable=False)

    # customers = db.relationship('Customer', backref=db.backref('invoice'))

    # return render_template('invoice.html')


class Invoice_Detail(db.Model):

    __tablename__="invoice_detail"

    invoice_detail_id = db.Column(db.Integer, primary_key=True)

    # invoice_number = db.Column(db.Unicode(50), db.ForeignKey('invoice.invoice_id'))
    # product_number = db.Column(db.Unicode(50), db.ForeignKey('product.product_id'))
    purchase_order_number = db.Column(db.Unicode(50))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    invoice = db.relationship('invoice', back_populates='products')
    product = db.relationship('product', back_populates='invoices')


class Customer(db.Model):

    __tablename__='customer'

    customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # customer_id = db.Column(db.Integer(11), primary_key=True), db.ForeignKey('invoice.invoice_id')
    # customer_type_id = db.Column(db.Integer(11), db.ForeignKey('customers.customer_type_id'), default ='0')
    # user_id = db.Column(db.Integer(11), default = '0')
    #customer_status = db.Column(db.Integer(2), nullable=False, default='0')
    created = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    # Information
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    phone2 = db.Column(db.String(30), nullable=True)
    company = db.Column(db.String(40), nullable=True)
    # Address
    address1 = db.Column(db.String(255), nullable=True)
    address2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(20), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    module_abbreviation =db.Column(db.String(4), nullable=True)

    ######STATUS#######
    active = db.Column(db.Boolean())
    ######STATUS#######

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    invoice = relationship('invoice', backref='invoice')

    # return render_template('show_user.html')


def seed_data():

    role_1=Role_ID(name='admin', description='master')
    role_2=Role_ID(name='estimator', description='staff estimator')
    role_3=Role_ID(name='customer', description='customer')

    db.session.add_all([role_1, role_2, role_3])
    db.session.commit()

    user1=User(fname='ninja', lname="Leslie", password='1234', email='her@her.com')
    user2=User(fname='bland', lname="Ninja", password='1234', email='me@her.com')
    user3=User(fname='test', lname="tester", password='1234', email='test@her.com')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    user_roles_admin=User_Roles(user_id=user1.user_id, role_id=role_1.role_id)
    user_roles_staff=User_Roles(user_id=user2.user_id, role_id=role_2.role_id)
    user_roles_customer=User_Roles(user_id=user3.user_id, role_id=role_3.role_id)

    db.session.add_all([user_roles_admin, user_roles_staff, user_roles_customer])
    db.session.commit()


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ecrm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


# class address(): 
#   address_id = db.Column(db.Integer(11), primary_key=True, nullable=False, autoincrement=True)
#   owner_id = db.Column(db.Integer(11), nullable=False, unique=True)
  
#   address_type = db.Column(db.String(100), nullable=True, unique=True)
#   address_1 = db.Column(db.String(50), nullable=False)
#   address_2 = db.Column(db.String(50), nullable=True)
#   state = db.Column(db.String(40), nullable=True)
#   city = db.Column(db.String(40), nullable=True)
#   country = db.Column(db.String(40), nullable=True)
#   zip_code = dbColumn(db.String(10), nullable=True)
#   date_created = db.Column(db.DateTime()),
#   date_updated = db.Column(db.DateTime()),
#   create_user_id = db.Column(db.Integer(11), nullable=False)
#   update_user_id = db.Column(db.Integer(11), default= '0')
#   create_ip_address = db.Column(db.String(15), nullable=False)
#   update_ip = db.Column(db.String(15), nullable=False)
#   module_abbreviation = db.Column(db.String(4), nullable=True)
#  # UNIQUE KEY owner_id (owner_id,owner_table,address_type),
#   owner_id_single = db.Column(db.Integer(11), db.ForeignKey('owner_id.owner_id')) 
#   # owner_table= db.Column(db.String(30), nullable=True, unique=True, db.ForeignKey('owner_table.owner_table'))


if __name__=="__main__":

    from server import app
    
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()