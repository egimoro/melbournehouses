import os

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('hse')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

ma = Marshmallow(app)

api = Api(app)
  

class House(db.Model):
    
    id = db.Column(db.Integer, primary_key=True) 
    hsetype = db.Column(db.String(1))
    rooms = db.Column(db.Integer())
    price = db.Column(db.Float())
    method = db.Column(db.String(2))
    date = db.Column(db.Date())
           
       


class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    suburb = db.Column(db.String())
    address = db.Column(db.String())
    postcode = db.Column(db.String(4))
    property_count = db.Column(db.Integer())
    distance = db.Column(db.Float())   
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))  
    houses = db.relationship('House', backref='location', uselist=False)        

    def __repr__(self):
        return self.suburb  



class HouseSchema(ma.ModelSchema):
    class Meta:
        model = House


class LocationSchema(ma.ModelSchema):  
    class Meta:
        model = Location
    

house_schema = HouseSchema()
houses_schema = HouseSchema(many=True)

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


class HelloMeBourne(Resource):  
    def get(self):
        return {'hello': 'Melbourne'}



class HouseList(Resource):
    def get(self):
        get_houses = House.query.all()
        results = houses_schema.dump(get_houses)

        return {'Number of houses': len(results), 'Houses': results}
       
    def post(self):

        data = request.get_json()
        house = House(hsetype=data['hsetype'], rooms= data['rooms'],
                                        price=data['price'], method=data['method'], date=data['date'])
        
        db.session.add(house)  
        db.session.commit()

        result = house_schema.dump(house)   

        return {'House added': result}

    
class LocationList(Resource):
    def get(self):
        get_locations = Location.query.all()
        results = locations_schema.dump(get_locations)

        return {'Number of locations': len(results), 'Location': results}
    
    def post(self):
    
        data = request.get_json()
        try:
             new_location = Location(suburb=data['suburb'], address=data['address'], 
                                postcode=data['postcode'], property_count=data['property_count'],
                                distance=data['distance'], house_id=data['house_id'])
        except:
            return {'Error': 'Bad Request'}, 400
     
           
        db.session.add(new_location)
        db.session.commit()   
        result = location_schema.dumps(new_location) 
        
        return {'Location added': result}     


class LocationRes(Resource):
    def get(self, pk):
        location = Location.query.get(pk)
        
        if location is None:
            return {'Error': 'Not found'}
        else:
            result = location_schema.dump(location)
            return {'Location': result}

    def delete(self, pk):
        location = Location.query.get(pk)
        
        if location is None:
            return {'Error': 'Not found'}
        else:
            db.session.delete(location)
            db.session.commit()

            return {'Message': 'Deleted'}

    def put(self, pk):
        data = request.get_json()
        location = Location.query.get_or_404(pk)

        location.suburb = data['suburb']
        location.address = data['address']
        location.postcode = data['postcode']
        location.property_count = data['property_count']
        location.distance = data['distance']

        result = location_schema.dump(location)

        return {'Updated': result}



class HouseRes(Resource):
    def get(self, pk):
        house = House.query.get(pk)
        
        if house is None:
            return {'Error': 'Not found'}    
        else:
            result = house_schema.dump(house)
            return {'Location': result}

    def delete(self, pk):
        house = House.query.get(pk)
        
        if house is None:
            return {'Error': 'Not found'}
        else:
            db.session.delete(house)
            db.session.commit()
            return {'Message': 'Deleted'} 
    
    def put(self, pk):
        data = request.get_json()
        house = House.query.get_or_404(pk)


        house.hsetype = data['hsetype']
        house.rooms = data['rooms']
        house.method = data['method']   
        house.price = data['price']
        house.date = data['date']
    
        
        db.session.commit()
        result = house_schema.dump(house)

        return {'House updated': result}


class HouseSearch(Resource):
    def get(self, hsetype):
        hsetype = House.query.filter(House.hsetype.ilike('%'+hsetype+'%')).all()
        result = houses_schema.dump(hsetype)
        
        return {'House type searched': result, 'Number of results': len(result)}
    

class LocationSearch(Resource):
    def get(self, address):
        address = Location.query.filter(Location.address.ilike('%'+address+'%')).all()
        result = locations_schema.dump(address)
       
        return {'Address searched': result, 'Number of results': len(result)}


api.add_resource(HelloMeBourne, '/')     
api.add_resource(HouseList, '/api/houses')
api.add_resource(HouseRes, '/api/houses/<string:pk>')
api.add_resource(LocationList, '/api/locations')     
api.add_resource(LocationRes, '/api/locations/<string:pk>') 
api.add_resource(HouseSearch, '/api/houses/search/<string:hsetype>')   
api.add_resource(LocationSearch, '/api/locations/search/<string:address>')   

if __name__ == '__main__':
    app.run(debug=True)
    