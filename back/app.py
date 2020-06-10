from flask import Flask
from flask import jsonify,request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JWT_SECRET_KEY'] = 'demofido'
jwt = JWTManager(app)

CORS(app)
from api import *

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
