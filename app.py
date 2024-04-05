# app.py

from flask import Flask
from routes import routes

app = Flask(__name__)

# Register the blueprint for todos routes
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
