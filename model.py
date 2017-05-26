from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask
db = SQLAlchemy()


class User(db.Model):

    __tablename__ ="users"

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

    # Account status
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    roles = db.relationship('Role_ID', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User user_id=%d, email=%s>' % (self.user_id, self.email)


class Role_ID(db.Model):
    """Role ID table."""

    __tablename__ ="roles"

    role_id = db.Column(db.Integer, 
                      primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User_Roles(db.Model):

    __tablename__="user_roles"

    user_role_id = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.role_id', ondelete='CASCADE'))



class Product(db.Model):

    __tablename__ ="product"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.Unicode(50), nullable=True)
    product_number = db.Column(db.String(10), nullable=False, unique=True)
    description = db.Column(db.Unicode(255))
    product_type = db.Column(db.Unicode(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.Unicode(500))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    
    jobs = db.relationship('Job', backref=db.backref('product', lazy='joined'), secondary='job_product')
    

class Job_Product(db.Model):

    __tablename__="job_product"

    jpid = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.product_id', ondelete='CASCADE'))
    job_id = db.Column(db.Integer(), db.ForeignKey('jobs.job_id', ondelete='CASCADE'))


class Job(db.Model):

    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, primary_key=True)
    product_quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    total = db.Column(db.Float(precision=10, decimal_return_scale=2, asdecimal=True))

    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())

    user = db.relationship('User', backref=db.backref('user_jobs'), foreign_keys=[user_id])
    customer = db.relationship('User', backref=db.backref('customer_jobs'), foreign_keys=[customer_id])


# ----------------------

class Invoice(db.Model):

    __tablename__ ="invoice"

    invoice_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    customer_id = db.Column(db.ForeignKey(u'customer.customer_id'), nullable=False, index=True)
    invoice_number = db.Column(db.Unicode(50), unique=True)
    invoice_created_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    invoice_due_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    modified = db.Column(db.DateTime())
    received_date = db.Column(db.DateTime())
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(u'users.user_id'), index=True)
    ##Ask Leslie
    # product = db.relationship('Invoice_Detail', back_populates="invoice")
    customers = db.relationship('Customer', backref=db.backref('invoice'))


class Invoice_Detail(db.Model):

    __tablename__ ="invoice_detail"

    invoice_detail_id = db.Column(db.Integer, primary_key=True, unique=True)

    invoice_number = db.Column(db.Unicode(50), db.ForeignKey('invoice.invoice_number'))
    product_number = db.Column(db.Unicode(50), db.ForeignKey('product.product_number'))
    purchase_order_number = db.Column(db.Unicode(50))
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    invoice = db.relationship('invoice', back_populates='products')
    product = db.relationship('product', back_populates='invoices')


class Customer(db.Model):

    __tablename__ ='Customer'

    customer_id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Information
    fname = db.Column(db.String(50), nullable=False)
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

    # Account status
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    modified = db.Column(db.DateTime())

    invoice = relationship('invoice', backref='invoice')


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


if __name__ == "__main__":

    from server import app
    
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()