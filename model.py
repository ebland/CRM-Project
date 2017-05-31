from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
db = SQLAlchemy()


class User(db.Model):

    __tablename__="users"

    user_id = db.Column(db.Integer(), autoincrement=True, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.String(2), nullable=True)

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
    product_name = db.Column(db.String(), nullable=True)
    product_number = db.Column(db.String(10))
    description = db.Column(db.Unicode(255))
    product_type = db.Column(db.Unicode(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.Unicode(500))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    module_abbreviation =db.Column(db.String(4), nullable=True)
    jobs = db.relationship('Job', backref=db.backref('product', lazy='joined'), secondary='job_product')


class Job(db.Model):

    __tablename__="jobs"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    quantity = db.Column(db.Integer(), nullable=True)
    module_abbreviation = db.Column(db.String(4), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    job_location = db.Column(db.String(100))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    total = db.Column(db.Float(precision=10, decimal_return_scale=2, asdecimal=True))

    # quote_id = db.Column(db.Integer(11), db.ForeignKey('quotes.quote_id'))
    # total_net_amount = db.Column(db.Integer(5), db.ForeignKey(total_net_amount.c_total_net_amount(10,2)))
    # staff_total_amount = db.Column(db.Integer(5), db.ForeignKey(staff_total_amount.c_staff_total_amount(10,2)))
    
    #Leslie, I want these to be updated with information about job adds and edits to update it underneath the user
    # update_user_id = db.Column(db.Integer(11), nullable=True)
    # create_user_id = db.Column(db.Integer(11), nullable=False)

    ######STATUS#######
    active = db.Column(db.Boolean())
    status = db.Column(db.String(20))
    date_due = db.Column(db.DateTime())
    #####STATUS#####

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())

    user = db.relationship('User', backref=db.backref('user_jobs'), foreign_keys=[user_id])
    customer = db.relationship('User', backref=db.backref('customer_jobs'), foreign_keys=[customer_id])

    

class Job_Product(db.Model):

    __tablename__="job_product"

    jpid = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id', ondelete='CASCADE'))
    job_id = db.Column(db.Integer(), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))

# ----------------------

class Invoice(db.Model):

    __tablename__="invoice"

    invoice_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    # customer_id = db.Column(db.Integer) 
    name = db.Column(db.String(90), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    module_abbreviation =db.Column(db.String(4), nullable=True)
    invoice_created_date = db.Column(db.DateTime())
    invoice_due_date = db.Column(db.DateTime())
    job_id = db.Column(db.String(11))
    date_paid = db.Column(db.String(11))
    date_sent = db.Column(db.String(11))
    product_quantity = db.Column(db.Integer())
    active = db.Column(db.String(11))
    phone = db.Column(db.String(11))
    location_address1 = db.Column(db.String(50))
    location_address2= db.Column(db.String(50))
    location_city = db.Column(db.String(50))
    location_state = db.Column(db.String(50))
# invoice = db.Column(db.ForeignKey('invoice.invoice_id'))
    #need to fix these relationships

    # update_user_id = db.Column(db.Integer(11), nullable=True)
    # create_user_id=db.Column(db.Integer(11), nullable=False)
    # customer_id = db.Column(db.Integer(11), db.ForeignKey('customer.customer_id'))
    # customers = db.relationship('Customer', backref=db.backref('invoice'))
    # user_id=db.Column(db.Integer())
    # return render_template('invoice.html')


class Invoice_Detail(db.Model):

    __tablename__="invoice_detail"

    invoice_detail_id = db.Column(db.Integer, primary_key=True)
    purchase_order_number = db.Column(db.Integer())
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    # invoice = db.relationship('Invoice', back_populates='product')
    # product = db.relationship('product', back_populates='invoices')
    invoice_number = db.Column(db.Integer(), db.ForeignKey('invoice.invoice_id'))
    product_number = db.Column(db.Integer(), db.ForeignKey('product.product_id'))




# class Customer(db.Model):

#     __tablename__='customer'

#     customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     customer_status = db.Column(db.Integer())
#     created = db.Column(db.DateTime())
#     modified = db.Column(db.DateTime())
#     email = db.Column(db.String(60), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     # Information
#     fname = db.Column(db.String(50), nullable=True)
#     lname = db.Column(db.String(50), nullable=False)
#     phone = db.Column(db.String(30), nullable=True)
#     phone2 = db.Column(db.String(30), nullable=True)
#     company = db.Column(db.String(40), nullable=True)
#     # Address
#     address1 = db.Column(db.String(255), nullable=True)
#     address2 = db.Column(db.String(255), nullable=True)
#     city = db.Column(db.String(100), nullable=True)
#     state = db.Column(db.String(20), nullable=True)
#     zip_code = db.Column(db.String(10), nullable=True)
#     module_abbreviation =db.Column(db.String(4), nullable=True)

#     ######STATUS#######
#     active = db.Column(db.Boolean())
#     ######STATUS#######

#     created_at = db.Column(db.DateTime())
#     modified = db.Column(db.DateTime())
    # user_id = db.Column(db.Integer())
    
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

    job_1=Job(name='project', user_id=user2.user_id, customer_id=user3.user_id, status="active")
    job_2=Job(name='big project', user_id=user2.user_id, customer_id=user3.user_id, status="quote_sent")
    job_3=Job(name='small project', user_id=user2.user_id, customer_id=user3.user_id, status="quote_requested")
    job_4=Job(name='bigger project', user_id=user2.user_id, customer_id=user3.user_id, status="invoice_sent")
    job_5=Job(name='biggest project', user_id=user2.user_id, customer_id=user3.user_id, status="completed")
    job_6=Job(name='smallest project', user_id=user2.user_id, customer_id=user3.user_id, status="active")

    db.session.add_all([job_1, job_2, job_3, job_4, job_5, job_6])
    db.session.commit()

    product_1=Product(product_number='12345678', product_name='good product')
    product_2=Product(product_number='11111111', product_name='big product')
    product_3=Product(product_number='22222222', product_name='small product')
    product_4=Product(product_number='33333333', product_name='bigger product')
    product_5=Product(product_number='44444444', product_name='biggest product')
    product_6=Product(product_number='42525252', product_name='biggest product')

    db.session.add_all([product_1, product_2, product_3, product_4, product_5, product_6])
    db.session.commit()

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ecrm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

#solution for address conflicts would be to use this as main then relate it to different modules 
#rather than have separate addresses (duplicates) under same user/customer table....

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
#   UNIQUE KEY owner_id (owner_id,owner_table,address_type),
#   owner_id_single = db.Column(db.Integer(11), db.ForeignKey('owner_id.owner_id')) 
#   owner_table= db.Column(db.String(30), nullable=True, unique=True, db.ForeignKey('owner_table.owner_table'))


if __name__=="__main__":

    from server import app
    
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()