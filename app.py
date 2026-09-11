import datetime
import os
from flask import Flask, jsonify, render_template, request
from groq import Groq

app = Flask(__name__)

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_msg = data.get('message','').strip()
    lower_msg = user_msg.lower()

    apps = {
        "youtube":"https://youtube.com","google":"https://google.com",
        "gmail":"https://mail.google.com","github":"https://github.com",
        "instagram":"https://instagram.com","chatgpt":"https://chat.openai.com"
    }
    for name,url in apps.items():
        if f"open {name}" in lower_msg or lower_msg==name:
            return jsonify({'reply':f'Opening {name.upper()}, Boss!','url':url})

    if not client:
        return jsonify({'reply':'Boss, GROQ_API_KEY missing in Render Environment.'})

    try:
        # 2026 NEW WORKING MODEL - Llama retired
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role":"system","content":"You are FRIDAY built by Boss Teja for DH². Reply same language as user. Short, witty, call him Boss."},
                {"role":"user","content":user_msg}
            ],
            max_tokens=150
        )
        return jsonify({'reply': completion.choices[0].message.content})
    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)[:150]}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
