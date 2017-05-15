from flask_sqlalchemy import SQLAlchemy

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
    added_date = db.Column(db.Date())
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    is_subscribed = db.Column(db.Enum('T', 'F'))


class Invoice(db.Model):

    __tablename__ ="invoice"

    id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    invoice_number = db.Column(db.Unicode(50), primary_key=True, unique=True)
    received_date = db.Column(db.Date, default=datetime.today())
    product = db.relationship('InvoiceDetail', back_populates="invoice")


class Product(db.Model):

    __tablename__ ="product"

    id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    product_number = db.Column(db.Unicode(50), primary_key=True, unique=True)
    description = db.Column(db.Unicode(255))
    product_type = db.Column(db.Unicode(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.Unicode(500))
    invoices = db.relationship('InvoiceDetail', back_populates='product')

    @classmethod
    def get_or_create(
        cls, product_number, session,
        description=None, product_type='Other', price=None,
    ):
        product = cls.query.get(product_number)
        if not product:
            product = cls(
                product_number=product_number,
                description=description,
                product_type=product_type,
                price=price,
            )
            session.add(product)
        return product

    @property
    def available_invoices(self):
        return [
            i for i in self.invoices if i.status in (
                'New', 'In Stock'
            )
        ]


class InvoiceDetail(db.Model):

     __tablename__ ="invoice_detail"

    id = db.Column(db.Integer,
                      primary_key=True, 
                      unique=True)
    invoice_number = db.Column(db.Unicode(50), db.ForeignKey('invoice.invoice_number'))
    product_number = db.Column(db.Unicode(50), db.ForeignKey('product.product_number'))
    purchase_order_number = db.Column(db.Unicode(50))
    status = db.Column(
        db.Enum(
            u'New', u'NOS', u'In Stock',
            u'Prototype', u'Returned',
        ),
        default=u'New'
    )
    in_stock = db.Column(db.Boolean, default=False)
    in_stock_date = db.Column(db.Date, nullable=True)
    product = db.relationship('Product', back_populates='invoices')
    invoice = db.relationship('Invoice', back_populates='products')


class Role(db.Model, Role):
    id = db.Column(db.Integer(), 
                      primary_key=True,
                      unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    class RolesUsers(db.Model):

     __tablename__ ="role_users"

    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),


class User(db.Model, User):

     __tablename__ ="user"

    id = db.Column(db.Integer, 
                      primary_key=True,
                      unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    start_date = db.Column(db.Date(), nullable=False)
    birth_date = db.Column(db.Date())
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))

    # Account status
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users

class Client(db.Model, User):

     __tablename__ ="client"

    id = db.Column(db.String(255), 
                      primary_key=True, 
                      unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    # Client Information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    added_date = db.Column(db.Date())
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    is_subscribed = db.Column(db.Enum('T', 'F'))

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///customersappdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."


