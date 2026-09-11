import os, time, json
from flask import Flask, jsonify, render_template, request
from groq import Groq
from datetime import datetime

app = Flask(__name__)
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

# Chat file - Render lo kuda save avvali ante /tmp use chestham
CHAT_FILE = "friday_memory.json"

def load_memory():
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE,'r',encoding='utf-8') as f:
                return json.load(f)
    except: pass
    return []

def save_memory(memory):
    try:
        with open(CHAT_FILE,'w',encoding='utf-8') as f:
            json.dump(memory[-100:], f, ensure_ascii=False) # last 100 save
    except: pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_history')
def get_history():
    return jsonify(load_memory())

@app.route('/clear_history', methods=['POST'])
def clear_history():
    save_memory([])
    return jsonify({'status':'cleared'})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_msg = data.get('message','').strip()
    lower_msg = user_msg.lower()
    history = data.get('history', [])

    apps = {"youtube":"https://youtube.com","google":"https://google.com","gmail":"https://mail.google.com","github":"https://github.com","instagram":"https://instagram.com","facebook":"https://facebook.com","chatgpt":"https://chat.openai.com","netflix":"https://netflix.com","hotstar":"https://hotstar.com"}
    for name,url in apps.items():
        if f"open {name}" in lower_msg or lower_msg==name:
            return jsonify({'reply':f'Opening {name.upper()}, Boss!','url':url})

    if not client:
        return jsonify({'reply':'GROQ key ledu.'})

    messages = [{"role":"system","content":"You are FRIDAY, built by Boss Teja. Indian female AI. SAME language as user. FULL DETAILED answer. Call Boss. Remember past chat."}]
    for h in history[-6:]:
        messages.append(h)
    messages.append({"role":"user","content":user_msg})

    for _ in range(3):
        try:
            c = client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages, max_tokens=800, temperature=0.8)
            reply = c.choices[0].message.content
            # SAVE TO SERVER MEMORY
            mem = load_memory()
            mem.append({"role":"user","content":user_msg,"time":str(datetime.now())[:19]})
            mem.append({"role":"assistant","content":reply,"time":str(datetime.now())[:19]})
            save_memory(mem)
            return jsonify({'reply': reply})
        except Exception as e:
            if "429" in str(e): time.sleep(2); continue
            return jsonify({'reply': f"Error: {str(e)[:150]}"})
    return jsonify({'reply':"10 sec aagi adugu Boss."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
