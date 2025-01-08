
import sqlite3

# Konfigurasi Flask
app = Flask(__name__)
CORS(app)

# API Key OpenAI
openai.api_key = "your-openai-api-key"

# Fungsi untuk menyimpan riwayat ke database
def save_to_db(user_message, bot_reply):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS chat (user TEXT, bot TEXT)")
    cursor.execute("INSERT INTO chat (user, bot) VALUES (?, ?)", (user_message, bot_reply))
    conn.commit()
    conn.close()

# Endpoint untuk chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"reply": "Tolong masukkan pesan!"})

    try:
        # Meminta respons dari OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response["choices"][0]["message"]["content"]
        
        # Simpan ke database
        save_to_db(user_message, bot_reply)
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Terjadi kesalahan: {str(e)}"})

if __name__ == '__main__':
    app.run(port=5000)
