from flask import Blueprint
from modelo.sensor import Sensor
from modelo.datos import Datos
from modelo.user import User
from modelo.prediccion import Prediccion
from flask import jsonify, json, make_response, request
from marshmallow import Schema, fields, ValidationError
from decimal import Decimal
from flask_cors import CORS
from json import dumps, loads
import uuid
import requests
from datetime import datetime
api = Blueprint('api', __name__)



CORS(api)
cors = CORS(api, resource={
    r"/*":{
        "origins":"*"
    }
})

class BaseSchema(Schema):
    ip= fields.String(required=True)
    nombre= fields.String(required=True)
    tipo = fields.String(required=True)

@api.route('/')
def home():
    return 'Hola api solar'

@api.route('/sensores')
def sensores():
    sensores = Sensor.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in sensores])}
                ),
                200,
            )

@api.route('/sensores/guardar',methods =['POST'])
def sensores_guardar():
    request_data = request.json
    
    schema = BaseSchema()
    #sensores = Sensor.query.all()
    try:
        # Validate request body against schema data types
        print(request_data)
        result = schema.load(request_data)
        
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400

    # Convert request body back to JSON str
    data_now_json_str = dumps(result)
    ip = request_data.get('ip')
    nombre = request_data.get('nombre')
    tipo = request_data.get('tipo')
    s = Sensor(nombre, True,str(uuid.uuid4()),ip, tipo)
    s.save()
    return make_response(
                jsonify(
                    {"message": "Se ha guardado", "code": 200}
                ),
                200,
            )

@api.route('/sensores/data/guardar')
def sensores_data():
    sen = Sensor.query.all()
    i = 0
    for row in sen:        
        #print(sen[0].ip)
        auxIp = "http://"+sen[i].ip+"/3"
        print(auxIp)
        data = requests.get(url=auxIp)
        sensor_data = data.json()
    #print(sensor_data["humedad"])
    #print("hola")
        dato = Datos(sensor_data["humedad"], True, str(uuid.uuid4()), str(datetime.now()), sen[i].id)
        dato.save()
        dato = Datos(sensor_data["temperatura"], True, str(uuid.uuid4()), str(datetime.now()), sen[i].id)
        dato.save()
        i = i + 1
    #sensores = Sensor.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200}
                ),
                200,
            )

@api.route('/datos')
def datos():
    datos1 = Datos.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in datos1])}
                ),
                200,
            )