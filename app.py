# app.py

from flask import Flask
from routes import routes
from models import db 

app = Flask(__name__)


# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:todo-admin@todo.ckgbjrurodq3.ap-south-1.rds.amazonaws.com:3306/to_do_app'  # Replace 'your_database_uri' with your actual URI

# Initialize SQLAlchemy with the Flask app
db.init_app(app)


# Register the blueprint for todos routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
