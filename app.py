import datetime
import os

from flask import Flask, jsonify, render_template, request
from flask import Flask

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def offline_reply():
    return (
        "I'm FRIDAY and I'm currently offline. "
        "I can still tell the time, open YouTube, or open Google for you, Boss."
    )


@app.route('/')
def home():
    return "FRIDAY is LIVE! - Your AI is Working"



@app.route('/ask', methods=['POST'])
def ask():
    payload = request.get_json(silent=True) or {}
    user_msg = str(payload.get('message', '')).strip()
    msg_lower = user_msg.lower()
    now = datetime.datetime.now()

    if not user_msg:
        return jsonify({'reply': 'Boss, I need a command or question.'})

    if 'youtube' in msg_lower:
        return jsonify({'reply': 'Opening YouTube Boss', 'action': 'youtube'})
    if 'google' in msg_lower:
        return jsonify({'reply': 'On it Boss', 'action': 'google'})
    if 'time' in msg_lower:
        return jsonify({'reply': f"It's {now.strftime('%I:%M %p')} Boss"})
    if 'who are you' in msg_lower or 'about friday' in msg_lower:
        return jsonify({'reply': 'I am FRIDAY, your AI assistant, Boss. Ready to help.'})

    if client is None:
        return jsonify({'reply': offline_reply()})

    try:
        chat = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are FRIDAY, female AI from Iron Man. For Teja. Call him Boss. Reply short, caring, smart.'
                },
                {'role': 'user', 'content': user_msg}
            ]
        )
        response = chat.choices[0].message.content
        return jsonify({'reply': response.strip() or offline_reply()})
    except Exception as exc:
        app.logger.exception('Groq request failed: %s', exc)
        return jsonify({'reply': offline_reply()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
