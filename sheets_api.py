import gspread
from google.oauth2.service_account import Credentials
import time

# Load API Credentials
creds = Credentials.from_service_account_file("saas-service-account.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_ID = "your_google_sheet_id"  # Replace with your actual Sheet ID
sheet = client.open_by_key("1oho8vHcU-rlN9x-Fi81IEuCbeCuvmVI_Sufjk7zQm0A").sheet1  # Select first sheet

# Define columns for different prompt types
PROMPT_COLUMNS = {
    "Normal Output": "C",
    "Chat/Search Prompt": "D",
    "Professional & Business Writing": "E",
    "Summarization": "F",
    "Creative Writing / Poetic Enhancement": "G",
    "Expanding Ideas": "H",
    "Simplifying Complex Text": "I",
    "Image Generation Prompt": "J",
    "Video Generation Prompt": "K",
    "Audio Generation Prompt (Music / Voiceover)": "L",
    "Image to Video Prompt": "M",
    "Text to Image Prompt": "N",
    "Image-to-3D Model Prompt": "O",
    "Image Enhancement Prompt": "P",
    "Video-to-Image Frames Prompt": "Q",
    "Music-to-Animation Prompt": "R",
    "Text-to-Website Design Prompt": "S",
    "Text-to-Infographic Prompt": "T",
    "Text-to-Game Character Prompt": "U",
    "Text-to-Logo Prompt": "V",
    "Text-to-API Generator Prompt": "W",
    "AI-Powered UI/UX Design Generator Prompt": "X"
}

# Ask user for input text
user_input = input("Enter your input text: ")

# Append user input to the sheet (Column A)
sheet.append_row([user_input])
print("\n✅ Input submitted! Processing...")

# Wait for Google Sheets formulas to process the data
time.sleep(3)  # Adjust time delay if needed

# Fetch all data again
data = sheet.get_all_values()

# Find the row where the new input was added
for row in reversed(data[1:]):  # Skipping header row
    if row[0] == user_input:
        translated_text = row[1]  # Column B contains translated text
        break
else:
    print("⚠ Error: Could not find processed data.")
    exit()

# Ask user to select the type of prompt
print("\n🔹 Select the prompt type:")
for idx, prompt_type in enumerate(PROMPT_COLUMNS.keys(), start=1):
    print(f"{idx}. {prompt_type}")

choice = int(input("\nEnter the number corresponding to the prompt type: "))
selected_prompt_type = list(PROMPT_COLUMNS.keys())[choice - 1]  # Get the corresponding column name
selected_column_index = ord(PROMPT_COLUMNS[selected_prompt_type]) - ord('A')  # Convert letter to index

# Get the processed prompt output from the selected column
prompt_output = row[selected_column_index]

# Display results
print(f"\n🎯 Showing results for: {selected_prompt_type}\n")
print(f"📝 User Input: {user_input}")
print(f"🌍 Translated: {translated_text}")
print(f"🎯 Generated Prompt: {prompt_output}\n")

print("✅ Done!")
