import os, time
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
    history = data.get('history', []) # chat history for full context

    # APP OPEN - Unlimited
    apps = {"youtube":"https://youtube.com","google":"https://google.com","gmail":"https://mail.google.com","github":"https://github.com","instagram":"https://instagram.com","facebook":"https://facebook.com","chatgpt":"https://chat.openai.com","netflix":"https://netflix.com","hotstar":"https://hotstar.com"}
    for name,url in apps.items():
        if f"open {name}" in lower_msg or lower_msg==name:
            return jsonify({'reply':f'Opening {name.upper()}, Boss! Ready!','url':url})

    if not client:
        return jsonify({'reply':'Boss GROQ key ledu.'})

    # Build messages with history for full answer
    messages = [{"role":"system","content":"You are FRIDAY, built by Boss Teja for DH². You are an Indian female AI. Reply in SAME language as user (Telugu if Telugu, English if English). Give FULL DETAILED answer, not short. Explain properly. Call user Boss Teja. Be friendly, witty, advanced like Tony Stark FRIDAY."}]
    # last 4 chat history add chey
    for h in history[-4:]:
        messages.append(h)
    messages.append({"role":"user","content":user_msg})

    for _ in range(3):
        try:
            c = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                max_tokens=800, # FULL ANSWER - 800 tokens
                temperature=0.8
            )
            return jsonify({'reply': c.choices[0].message.content})
        except Exception as e:
            if "429" in str(e):
                time.sleep(2)
                continue
            return jsonify({'reply': f"Error Boss: {str(e)[:150]}"})
    return jsonify({'reply':"Boss 10 sec aagi malli adugu, limit touch ayyindi."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
