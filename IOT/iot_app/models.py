from iot_app import db

class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    overridden = db.Column(db.Boolean, default=False)

class Override(db.Model):
    __tablename__ = 'override'

    id = db.Column(db.Integer, primary_key=True)
    enabled = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Override {self.sensor_id}: {'Active' if self.active else 'Inactive'}>"
