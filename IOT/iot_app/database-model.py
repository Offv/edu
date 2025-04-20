from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    overridden = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<SensorData {self.sensor_id} at {self.timestamp}>"

class Override(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)
    simulated_value = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Override {self.sensor_id}: {'Active' if self.active else 'Inactive'}>"
