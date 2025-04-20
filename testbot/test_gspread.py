import gspread
from google.oauth2.service_account import Credentials

# ID Google Sheets
SHEET_ID = "1MWfn7YOTOazBZCxehDUGmSRgRvpRhQYQMvgYq9Ubyp4"  # Подставь свой ID

# Подключение к сервисному аккаунту
creds = Credentials.from_service_account_file("service-account.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Открытие Google Sheets
sheet = client.open_by_key(SHEET_ID).sheet1

# Чтение данных (первые 5 строк)
data = sheet.get_all_values()
print("Содержимое таблицы:", data)

# Запись тестовых данных
sheet.update_cell(2, 2, "Тест")  # Вставит "Тест" в ячейку B2
print("Данные обновлены!")
