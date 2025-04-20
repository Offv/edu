from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///v_plc_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inlet_flow = db.Column(db.Float)
    inlet_temp = db.Column(db.Float)
    outlet_flow = db.Column(db.Float)
    outlet_temp = db.Column(db.Float)
    heater1_temp = db.Column(db.Float)
    heater2_temp = db.Column(db.Float)
    pid_setpoint = db.Column(db.Float)
    pid_actual = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.now())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    # Query the latest data from the database
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()

    if latest_data:
        return jsonify({
            'inlet_flow': latest_data.inlet_flow,
            'inlet_temp': latest_data.inlet_temp,
            'outlet_flow': latest_data.outlet_flow,
            'outlet_temp': latest_data.outlet_temp,
            'heater1_temp': latest_data.heater1_temp,
            'heater2_temp': latest_data.heater2_temp,
            'pid_setpoint': latest_data.pid_setpoint,
            'pid_actual': latest_data.pid_actual
        })
    else:
        return jsonify({'error': 'No data found'})

if __name__ == '__main__':
    app.run(debug=True)
