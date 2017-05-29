
def connect_to_db(app):
    """Connect to my Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ecrm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

"""experiment to see what run.py does"""

import os
import sys
sys.path.append(os.path.dirname(__name__))
#os.environ['DATABASE_URL'] = <URL>

print("")
print("Elizabeth Bland Hackbright Project CRM 2017")
