from flask import Flask, request
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'ajmal'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')  
api.add_resource(ItemList, '/items')    
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True) 
