import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ensure to provide the correct path to your existing database file
DB_FILE = os.path.join(os.getcwd(), 'v_plc_db.db')  # Assuming it's in the current working directory
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PLCData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(50), nullable=False)

@app.route('/')
def service_page():
    try:
        data = PLCData.query.all()
        return render_template('service.html', data=data)
    except Exception as e:
        return f"An error occurred: {e}", 500



@app.route('/get_data', methods=['GET'])
def get_data():
    """Fetch all PLC data values."""
    try:
        data = PLCData.query.all()
        return jsonify([{ "name": d.name, "value": d.value } for d in data])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/update_value', methods=['POST'])
def update_value():
    """Update a specific value in the database."""
    data = request.json
    try:
        variable_name = data.get('name')
        new_value = int(data.get('value'))  # Ensure the value is an integer

        # Fetch the PLCData entry and update it
        plc_entry = PLCData.query.filter_by(name=variable_name).first()
        if not plc_entry:
            return jsonify({'status': 'error', 'message': f'Variable {variable_name} not found.'}), 404

        if new_value not in [0, 1]:
            return jsonify({'status': 'error', 'message': 'Value must be 0 or 1.'}), 400

        plc_entry.value = new_value
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Value updated successfully.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Ensure database and table creation happens within an app context
    with app.app_context():
        db.create_all()  # Only creates tables if they don't already exist
    app.run(debug=True)
