from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# מפתח ה-API שלך
API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/', methods=['GET'])
def home():
    return "הבוט פעיל!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json  # מקבל הודעה מגוגל צ'אט
        if not data or "message" not in data or "text" not in data["message"]:
            return jsonify({"text": "לא התקבלה הודעה תקינה."})

        user_message = data["message"]["text"]  # שליפת הטקסט שנשלח
        ai_response = get_ai_response(user_message)  # שליחת הודעה ל-Groq

        return jsonify({"text": ai_response})  # שליחת תשובה חזרה לצ'אט

    except Exception as e:
        return jsonify({"text": f"שגיאה: {str(e)}"})

def get_ai_response(message):
    """ פונקציה ששולחת את ההודעה ל-Groq API ומקבלת תשובה """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "שגיאה בקבלת תשובה מהבינה המלאכותית."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
