import sqlite3

# Database file
DB_FILE = "v_plc_db.db"

# Create and set up the database schema
def setup_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create sensor_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            heater1_temp REAL,
            heater2_temp REAL,
            pid_setpoint REAL,
            pid_actual REAL,
            inlet_temp REAL,
            outlet_temp REAL,
            outdoor_temp REAL,
            inlet_pressure REAL,
            outlet_pressure REAL,
            inlet_flow REAL,
            outlet_flow REAL
        );
    """)

    # Create system_states table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            fan_running INTEGER CHECK (fan_running IN (0, 1)),
            flow_good INTEGER CHECK (flow_good IN (0, 1)),
            main_enable INTEGER CHECK (main_enable IN (0, 1)),
            system_ready INTEGER CHECK (system_ready IN (0, 1)),
            heater1_stages TEXT,
            heater2_stages TEXT
        );
    """)

    # Create manual_controls table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manual_controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            heater1_toggle TEXT,
            heater2_toggle TEXT
        );
    """)

    # Create logs table (optional, for debugging and events)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            log_message TEXT NOT NULL,
            log_type TEXT CHECK (log_type IN ('INFO', 'WARNING', 'ERROR')) NOT NULL
        );
    """)

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print(f"Database {DB_FILE} has been set up successfully!")

# Run the setup
if __name__ == "__main__":
    setup_database()
