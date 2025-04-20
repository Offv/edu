import re
import os
import gspread
from google.oauth2.service_account import Credentials
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Подключение к Slack API
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Подключение к Google Sheets
SHEET_ID = "1MWfn7YOTOazBZCxehDUGmSRgRvpRhQYQMvgYq9Ubyp4"
SERVICE_ACCOUNT_FILE = "service-account.json"

# Настройка учетных данных
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1  # Открываем первый лист

# Карта строк в таблице
ROW_MAPPING = {
    "Generator 1": 2,
    "Generator 2": 3,
    "Generator 3": 4,
    "Spuds HPU": 5,
    "Boom HPU": 6,
    "Compressor": 7,
    "Main Blower Port": 8,
    "Main Blower Stbd": 9,
    "Zero Air Compressor": 10,
    # "Fuel Cell": 11,  # Future use
}

# Регулярные выражения
equipment_pattern = r"(?P<equipment>Generator 1|Generator 2|Generator 3|Spuds HPU|Boom HPU|Compressor|Main Blower Port|Main Blower Stbd|Zero Air Compressor)\s*(\d+)\s*hrs"
stax_pattern = r"STAX (\d+)"

@app.event("message")
def handle_message_events(event, say):
    text = event.get("text", "")
    bot_id = event.get("bot_id", "")
    timestamp = event.get("ts", "")

    if not bot_id:
        print("Message not from a bot, ignoring.")
        return

    # Determine STAX number from bot_id (replace with actual mapping if needed)
    stax_match = re.search(stax_pattern, text)
    if not stax_match:
        print("No STAX number found, ignoring.")
        return

    stax_number = int(stax_match.group(1))
    col_index = stax_number

    # Update A20 with timestamp (as date)
    sheet.update_cell(20, stax_number, timestamp)

    # Extract equipment data
    matches = re.findall(equipment_pattern, text)
    if not matches:
        print("No equipment data found.")
        return

    print(f"Updating STAX {stax_number} data...")

    for equipment, hours in matches:
        row_index = ROW_MAPPING.get(equipment)
        if row_index:
            current_value = sheet.cell(row_index, col_index).value
            if current_value != hours:
                sheet.update_cell(row_index, col_index, hours)
                #sheet.update_cell(row_index, col_index + 1, timestamp)

    print(f"STAX {stax_number} updated successfully.")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()
