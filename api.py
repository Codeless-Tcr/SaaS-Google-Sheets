from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Google Sheets Integration
creds = Credentials.from_service_account_file("saas-service-account.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)
SPREADSHEET_ID = "your_google_sheet_id"  # Replace with your actual Sheet ID
sheet = client.open_by_key("1oho8vHcU-rlN9x-Fi81IEuCbeCuvmVI_Sufjk7zQm0A").sheet1  # Select first sheet

# Define column mapping
PROMPT_COLUMNS = {
    "Normal Output": "C",
    "Chat/Search Prompt": "D",
    "Professional & Business Writing": "E",
    "Summarization": "F",
    "Creative Writing/Poetic Enhancement": "G",
    "Expanding Ideas": "H",
    "Simplifying Complex Text": "I",
    "Image Generation Prompt": "J",
    "Video Generation Prompt": "K",
    "Audio Generation Prompt (Music / Voiceover)": "L",
    "Image to Video Prompt": "M",
    "Text to Image Prompt": "N",
    "Image to 3D Model Prompt": "O",
    "Image Enhancement Prompt": "P",
    "Video to Image Frames Prompt": "Q",
    "Music to Animation Prompt": "R",
    "Text to Website Design Prompt": "S",
    "Text to Infographic Prompt": "T",
    "Text to Game Character Prompt": "U",
    "Text to Logo Prompt": "V",
    "Text to API Generator Prompt": "W",
    "AI-Powered UI/UX Design Generator Prompt": "X"
}

@app.route("/generate_prompt", methods=["POST"])
def generate_prompt():
    data = request.json
    user_input = data.get("input")  # Get user input
    prompt_type = data.get("type")  # Get selected prompt type

    if not user_input or not prompt_type:
        return jsonify({"error": "Missing required fields"}), 400

    # Append user input to Google Sheets (Column A)
    sheet.append_row([user_input])

    # Fetch all data
    all_data = sheet.get_all_values()
    headers = all_data[0]  # First row is headers

    if prompt_type in PROMPT_COLUMNS:
        column_letter = PROMPT_COLUMNS[prompt_type]
        column_index = headers.index(prompt_type)  # Find the column index

        # Get the last row of data
        last_row = all_data[-1]  # Fetch latest user input row
        generated_prompt = last_row[column_index]  # Get prompt output

        return jsonify({
            "input": user_input,
            "prompt_type": prompt_type,
            "generated_prompt": generated_prompt
        })

    return jsonify({"error": "Invalid prompt type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
