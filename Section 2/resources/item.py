from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float, required=True, help="This field can't be left blank")


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name) 
        if item:
            return item.json()
        return { 'message': 'Item not found' }, 404 
   

    def post(self, name):
        if ItemModel.find_by_name(name):
            return { 'message': f"An item with the name {name} already exists" }    
        
        data = Item.parser.parse_args()

        item =  ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred while inserting the item"}, 500

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item has been deleted'}


    def put(self, name):      
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items = list(map(lambda x: x.json(), ItemModel.query.all()))

        # we can do it with list comprehension also, [ item.json() for item in  ItemModel.query.all() ]

        return {'items': items }