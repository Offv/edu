import sqlite3

DB_FILE = 'v_plc_db.db'

def initialize_db():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plc_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    ''')

    # List of initial variables
    variables = [
        "HTRA_1Pulse_On", "HTRA_2_On", "HTRA_3_On", "HTRA_4_On", "HTRA_5_On",
        "HTRB_1Pulse_On", "HTRB_2_On", "HTRB_3_On", "HTRB_4_On", "HTRB_5_On",
        "HTR.PID_Tpv", "HTR.OT.A_Tpv", "HTR.OT.B_Tpv", "MSO_dp_Heater",
        "MSO_T_Heater_C", "MSO_T_Heater", "MSO_P_Heater", "MSO_F2_Heater",
        "MSO_F_Heater", "HTR_Auto", "HTR_Count", "HTR.PID_%", "HTR_RESET",
        "HTR.PID_Tsp", "HTR_Pulse_width", "HTR_Pulse", "HTR_KP", "HTR_KI",
        "HTR_KD", "HTR_Pause", "HTR.OT.A_Tsp", "HTR.OT.B_Tsp",
        "HTR_PID_DecrementTimeSP", "HTR_PID_IncrementTimeSP", "HTR_PID_IncrementTime",
        "HTR_PID_DecrementTime", "MSO_F2_Low", "MSO_F2_LowSP"
    ]

    # Insert variables with default values
    for variable in variables:
        cursor.execute('INSERT OR IGNORE INTO plc_data (name, value) VALUES (?, ?)', (variable, '0'))

    connection.commit()
    connection.close()
    print("Database initialized with default values.")

if __name__ == '__main__':
    initialize_db()
