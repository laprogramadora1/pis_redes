from app import db
from modelo.sensor import Sensor
from flask import jsonify

class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Double)
    estado = db.Column(db.Boolean, default=True)
    fecha = db.Column(db.DateTime)
    external_id = db.Column(db.String(100))
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id'),nullable=False)
    

    def __init__(self, valor, estado, external_id, fecha, id_sensor):
        self.valor = valor
        self.estado = estado
        self.fecha = fecha
        self.external_id = external_id
        self.id_sensor = id_sensor 
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'fecha':self.fecha,
           'valor' : self.valor, 
           'estado' : self.estado
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    @property
    def serialize_id(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'valor':self.valor,
           'estado' : self.estado,
           'sensor' : self.sensor.external_id
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def getSensor(id):
        from modelo.sensor import Sensor        
        senso = Sensor.query.get(id)
        return  jsonify(senso.serialize())