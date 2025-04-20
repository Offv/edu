import random
import time
import sqlite3

# Path to your database
DB_FILE = "v_plc_db.db"

def simulate_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        while True:
            # Fetch all current values from the database
            cursor.execute("SELECT name, value FROM plc_data")
            rows = cursor.fetchall()

            data = {row[0]: float(row[1]) if row[1].replace('.', '', 1).isdigit() else row[1] for row in rows}

            # Update values that can be randomized
            for name, value in data.items():
                if name not in [
                    "HTR.OT.A_Tsp", "HTR.OT.B_Tsp",
                    "HTRA_1Pulse_On", "HTRA_2_On", "HTRA_3_On", "HTRA_4_On", "HTRA_5_On",
                    "HTRB_1Pulse_On", "HTRB_2_On", "HTRB_3_On", "HTRB_4_On", "HTRB_5_On",
                    "HTR_Pause", "MSO_F2_Low", "HTR_Auto", "HTR_RESET", "HTR_Count"
                ]:
                    if isinstance(value, float):
                        # Randomize sensor values
                        new_value = round(value + random.uniform(-1, 1), 2)
                        cursor.execute("UPDATE plc_data SET value = ? WHERE name = ?", (new_value, name))

            # Logic-controlled variables
            if data.get("MSO_F2_Heater", 0) > data.get("MSO_F2_LowSP", 0):
                cursor.execute("UPDATE plc_data SET value = ? WHERE name = ?", ("1", "MSO_F2_Low"))
            else:
                cursor.execute("UPDATE plc_data SET value = ? WHERE name = ?", ("0", "MSO_F2_Low"))

            conn.commit()
            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        conn.close()
def simulate_values():
    with app.app_context():
        data_entries = PLCData.query.all()
        for entry in data_entries:
            if not entry.manual_override:  # Skip manual overrides
                entry.value = random.uniform(0, 1)  # Example simulation logic
        db.session.commit()
if __name__ == "__main__":
    simulate_data()
