import datetime
import os
from flask import Flask, jsonify, render_template, request
from groq import Groq

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    msg = str(data.get('message','')).strip()
    low = msg.lower()
    now = datetime.datetime.now()

    if 'youtube' in low:
        return jsonify({'reply': 'Opening YouTube, Boss.', 'action': 'youtube'})
    if 'google' in low:
        return jsonify({'reply': 'Opening Google, Boss.', 'action': 'google'})
    if 'time' in low:
        return jsonify({'reply': f"It's {now.strftime('%I:%M:%S %p')}, Boss."})
    if 'about friday' in low or 'who are you' in low:
        return jsonify({'reply': "I am FRIDAY, your AI assistant, built by Boss Teja. Ready to help."})

    if not client:
        return jsonify({'reply': "I'm FRIDAY and I'm currently offline. I can still tell the time, open YouTube, or open Google for you, Boss."})
    try:
        chat = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[
                {'role':'system','content':'You are FRIDAY, female AI from Iron Man, for Teja. Call him Boss. Short, smart, loving.'},
                {'role':'user','content': msg}
            ]
        )
        return jsonify({'reply': chat.choices[0].message.content})
    except:
        return jsonify({'reply': "I'm FRIDAY and I'm currently offline. I can still tell the time, open YouTube, or open Google for you, Boss."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
