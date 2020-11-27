from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'ajmal'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float, required=True, help="This field can't be left blank")


    @jwt_required()
    def get(self, name):
        item = next(filter(lambda a: a['name'] == name, items), None)
        return {'item': item}, 200 if item else 404   

    def post(self, name):
        if next(filter(lambda a: a['name'] == name, items), None):
            return f"An item with name {name} already exists", 400       


        
        data = Item.parser.parse_args()
        item =  { 'name': name, 'price': data['price'] }
        items.append(item)   
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x : x['name'] != name, items))
        return { "message": "item deleted" }

    def put(self, name):       
        data = Item.parser.parse_args()
        item = next(filter(lambda a : a['name'] == name, items), None)
        if item is None:
            item =  { 'name': name, 'price': data['price'] }
            items.append(item)    
        else:
            item.update(data)

        return item



class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')  
api.add_resource(ItemList, '/items')    
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True) 
