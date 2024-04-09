# script.py

from flask import Flask
from models import db

# Create a Flask application instance
app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:todo-admin@todo.ckgbjrurodq3.ap-south-1.rds.amazonaws.com:3306/to_do_app'

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Define a function to create tables
def create_tables():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Tables created successfully!")

# Call the function to create tables
create_tables()
