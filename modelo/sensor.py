from app import db
from flask import jsonify
import enum
class TipoEnum(enum.Enum):
    TEMPERATURA = "TEMPERATURA"
    HUMEDAD = "HUMEDAD"
    PRESION = "PRESION"
    TEMPERATURA_HUMEDAD = "TEMPERATURA_HUMEDAD"

    def getValue(self):
        return self.value
    def __json__(self):
        return self.value

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(100))
    tipo = db.Column(db.Enum(TipoEnum))
    ip = db.Column(db.String(100))
    #cantones = db.relationship('Canton', backref='provincia', lazy=True)

    def __init__(self, nombre, estado, external_id, ip, tipo):
        self.nombre = nombre
        self.estado = estado
        self.external_id = external_id 
        self.ip = ip
        self.tipo = tipo
    
    
    def getNombre(self):
        return self.nombre
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'external'         : self.external_id,
           'nombre':self.nombre,
           'estado' : self.estado,
           'ip' : self.ip,
           'tipo' : self.tipo.getValue()
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    def save(self):
        db.session.add(self)
        db.session.commit()
    def getListEnum():
        lista = []
        for data in TipoEnum:
            lista.append({"key":data.name,"value":data.value})            
        return lista