import datetime
import os
from flask import Flask, jsonify, render_template, request
from groq import Groq

app = Flask(__name__)

# SECURE METHOD: Key Render Environment nundi vastundi
# GitHub lo key kanipinchadu - 100% Safe
GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_KEY:
    try:
        client = Groq(api_key=GROQ_KEY)
        print("FRIDAY: Groq Connected Successfully - DH² Core Online")
    except Exception as e:
        print(f"FRIDAY: Groq Init Failed: {e}")
else:
    print("FRIDAY: WARNING - GROQ_API_KEY not in Environment")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_msg = data.get('message', '').strip()
    lower_msg = user_msg.lower()

    # F2.0 - ALL APPS
    apps = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "instagram": "https://instagram.com",
        "chatgpt": "https://chat.openai.com",
        "maps": "https://maps.google.com",
        "drive": "https://drive.google.com",
        "netflix": "https://netflix.com",
        "spotify": "https://open.spotify.com",
        "whatsapp": "https://web.whatsapp.com"
    }

    for name, url in apps.items():
        if f"open {name}" in lower_msg or f"{name} open" in lower_msg or lower_msg == name:
            if any(x in lower_msg for x in ["chey", "cheyyi", "ela", "enti"]):
                reply = f"{name.upper()} open chesthunna Boss!"
            else:
                reply = f"Opening {name.upper()}, Boss!"
            return jsonify({'reply': reply, 'url': url})

    if any(x in lower_msg for x in ["time", "samayam"]):
        now = datetime.datetime.now().strftime("%I:%M %p, %d %B")
        return jsonify({'reply': f"Time is {now}, Boss. DH² Core perfect."})

    if "about" in lower_msg or "who are you" in lower_msg:
        return jsonify({'reply': "I am FRIDAY, built by Boss Teja under DH². 80% movie level ready!"})

    # F1.0 - AI BRAIN (Secure)
    if not client:
        return jsonify({'reply': "Boss, GROQ_API_KEY Render > Environment lo add chey. App open matram work avthundi."})

    try:
        system_prompt = """
        You are FRIDAY, built by Boss Teja for DH².
        1. Reply in SAME language user speaks (Telugu/Hindi/English auto-detect).
        2. Personality: Sarcastic, witty, short 1-2 lines, 80% like Marvel FRIDAY. Call him Boss.
        3. Never say you are Meta AI. You are FRIDAY.
        4. Keep under 25 words.
        """

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.8,
            max_tokens=120
        )
        return jsonify({'reply': completion.choices[0].message.content})

    except Exception as e:
        return jsonify({'reply': f"Boss, link slow. Error: {str(e)[:100]}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
