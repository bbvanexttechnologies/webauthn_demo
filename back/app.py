from flask import Flask
from flask import jsonify,request
from flask_cors import CORS
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
from api import *

if __name__ == '__main__':
    app.run(debug=True)
