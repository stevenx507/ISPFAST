from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ip_address = db.Column(db.String(15))
    mac_address = db.Column(db.String(17))
    plan_speed = db.Column(db.Integer, default=100)
    plan_price = db.Column(db.Float, default=450.0)
    is_active = db.Column(db.Boolean, default=True)
