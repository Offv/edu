from flask import request, jsonify
from datetime import datetime
from models import db, SensorData, Override

@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    sensor_id = data.get('sensor_id')
    value = data.get('value')

    # Check for override
    override = Override.query.filter_by(sensor_id=sensor_id).first()
    if override and override.active:
        value = override.simulated_value

    new_data = SensorData(
        sensor_id=sensor_id,
        timestamp=datetime.utcnow(),
        value=value,
        overridden=bool(override and override.active)
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data received", "data": value}), 201

@app.route('/override', methods=['POST'])
def set_override():
    data = request.json
    sensor_id = data.get('sensor_id')
    active = data.get('active')
    simulated_value = data.get('simulated_value')

    override = Override.query.filter_by(sensor_id=sensor_id).first()
    if not override:
        override = Override(sensor_id=sensor_id)

    override.active = active
    override.simulated_value = simulated_value
    db.session.add(override)
    db.session.commit()
    return jsonify({"message": "Override updated"}), 200
