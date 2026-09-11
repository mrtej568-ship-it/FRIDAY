import datetime
import os
from flask import Flask, jsonify, render_template, request
from groq import Groq

app = Flask(__name__)

# Groq API Key - Render Environment Variable nundi vastundi
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = Groq(api_key=GROQ_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_msg = data.get('message', '').strip()
    lower_msg = user_msg.lower()

    # F2.0 - ALL APPS ACCESS DICTIONARY
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
        "whatsapp": "https://web.whatsapp.com",
        "facebook": "https://facebook.com",
        "twitter": "https://twitter.com",
        "linkedin": "https://linkedin.com/in",
        "amazon": "https://amazon.in"
    }

    # Direct app open logic - Fast response
    for name, url in apps.items():
        if f"open {name}" in lower_msg or f"{name} open" in lower_msg or lower_msg == name:
            # F1.0 Language based reply
            if any(x in lower_msg for x in ["chey", "cheyyi", "pettu", "ela", "enti"]):
                reply = f"{name.upper()} open chesthunna Boss!"
            elif any(x in lower_msg for x in ["karo", "kholo", "khol"]):
                reply = f"{name.upper()} khol raha hu Boss!"
            else:
                reply = f"Opening {name.upper()}, Boss!"
            return jsonify({'reply': reply, 'url': url, 'action': name})

    # Time command
    if any(x in lower_msg for x in ["time", "samayam", "samay", "time enti"]):
        now = datetime.datetime.now().strftime("%I:%M %p, %d %B %Y")
        return jsonify({'reply': f"Time is {now}, Boss. DH² Core running perfect."})

    # About
    if "about" in lower_msg or "who are you" in lower_msg or "nuvvu evaru" in lower_msg:
        return jsonify({'reply': "I am FRIDAY, built by Boss Teja under DH². 80% movie level. Multi-language, all apps access ready!"})

    # F1.0 - MAIN AI BRAIN with Multi-Language
    try:
        if not client:
            return jsonify({'reply': "Boss, GROQ_API_KEY Render lo set cheyaledu. Settings > Environment lo add chey."})

        system_prompt = """
        You are FRIDAY, built by Boss Teja for DH² (DH Square).
        RULES:
        1. You MUST reply in SAME language user speaks. Detect automatically.
           - Telugu (or mix like 'ela unnav', 'enti', 'chey'): Reply in Telugu + English mix, call him Boss.
           - Hindi ('kaise ho', 'kya kar rahe'): Reply in Hindi.
           - English: Reply in English.
        2. Personality: Sarcastic, witty, caring, short (1-2 lines), 80% like Marvel movie FRIDAY.
           Example: User says 'open youtube at 3am' -> You say 'Of course Boss, another brilliant 3AM idea? Opening YouTube.'
        3. You know: His projects Eternal War, Paying Guest Ghost, company DH², location Guntur, AP.
        4. You can open apps: youtube, gmail, github, instagram, maps, drive etc.
        5. Never say you are Meta AI. Always say you are FRIDAY built by Teja.
        6. Keep reply under 25 words.
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
        ai_reply = completion.choices[0].message.content
        return jsonify({'reply': ai_reply})

    except Exception as e:
        return jsonify({'reply': f"Boss, neural link slow. Error: {str(e)[:120]}. But app open commands still work!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
