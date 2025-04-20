import sqlite3
import random
import time
from datetime import datetime

# Database file
DB_FILE = "v_plc_db.db"

# Define realistic data ranges for simulation
DATA_RANGES = {
    "heater1_temp": (300, 400),  # Heater 1 temperature range (°F)
    "heater2_temp": (300, 400),  # Heater 2 temperature range (°F)
    "pid_setpoint": (350, 380),  # PID setpoint (°F)
    "pid_actual": (345, 375),    # PID actual temperature (°F)
    "inlet_temp": (100, 150),    # Inlet air temperature (°F)
    "outlet_temp": (150, 200),   # Outlet air temperature (°F)
    "outdoor_temp": (30, 100),   # Outdoor temperature (°F)
    "inlet_pressure": (0.5, 1.5),# Inlet pressure (psi)
    "outlet_pressure": (0.8, 1.8),# Outlet pressure (psi)
    "inlet_flow": (600, 800),    # Inlet flow (CFM)
    "outlet_flow": (600, 800)    # Outlet flow (CFM)
}

# Generate random data within ranges
def generate_random_data():
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **{key: round(random.uniform(*value), 2) for key, value in DATA_RANGES.items()}
    }
    return data

# Insert data into the database
def insert_sensor_data(data):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (
            timestamp, heater1_temp, heater2_temp, pid_setpoint, pid_actual,
            inlet_temp, outlet_temp, outdoor_temp, inlet_pressure,
            outlet_pressure, inlet_flow, outlet_flow
        ) VALUES (
            :timestamp, :heater1_temp, :heater2_temp, :pid_setpoint, :pid_actual,
            :inlet_temp, :outlet_temp, :outdoor_temp, :inlet_pressure,
            :outlet_pressure, :inlet_flow, :outlet_flow
        )
    """, data)
    connection.commit()
    connection.close()

# Run the simulator
def run_simulator():
    print("Starting data simulator...")
    while True:
        data = generate_random_data()
        insert_sensor_data(data)
        print(f"Inserted data: {data}")
        time.sleep(5)  # Wait 5 seconds before generating the next data point

if __name__ == "__main__":
    run_simulator()
