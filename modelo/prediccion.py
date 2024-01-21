from app import db



class Prediccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))    
    tipo_predicccion = db.Column(db.String(100))#llueve, no llueve, sol, etc
    valor = db.Column(db.Double)
    fecha = db.Column(db.DateTime)
    external_id = db.Column(db.String(100))
    #cantones = db.relationship('Canton', backref='provincia', lazy=True)

    def __init__(self, nombre, valor, external_id, tipo_predicccion):
        self.nombre = nombre
        self.tipo_predicccion = tipo_predicccion
        self.valor = valor        
        self.external_id = external_id 
    
    
    def getNombre(self):
        return self.nombre
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'external'         : self.external_id,
           'nombre':self.nombre,
           'tipo_predicccion' : self.tipo_predicccion,
           'valor' : self.valor,
           'fecha' : self.fecha
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }