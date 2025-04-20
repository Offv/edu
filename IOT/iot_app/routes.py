from flask import Blueprint, request, jsonify
from iot_app import db
from iot_app.models import SensorData, Override
from datetime import datetime

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

# Route to receive sensor data and store it in the database
@main.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()

    # Validate required data
    if not data or 'value' not in data or 'timestamp' not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Create SensorData object and save to DB
    try:
        timestamp = datetime.fromisoformat(data['timestamp'])
        value = float(data['value'])
        overridden = False  # Initially, no override

        new_sensor_data = SensorData(timestamp=timestamp, value=value, overridden=overridden)
        db.session.add(new_sensor_data)
        db.session.commit()

        return jsonify({"message": "Sensor data received", "id": new_sensor_data.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to receive override signal and enable or disable simulation
@main.route('/override', methods=['POST'])
def set_override():
    data = request.get_json()

    # Validate required data
    if not data or 'enabled' not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Enable/Disable override in the database
    try:
        override = Override.query.first()  # Assuming one global override
        if not override:
            override = Override(enabled=data['enabled'], created_at=datetime.utcnow())
            db.session.add(override)
        else:
            override.enabled = data['enabled']

        db.session.commit()

        return jsonify({"message": "Override updated", "enabled": override.enabled}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
