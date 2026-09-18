import os
import telebot
from google import genai
from groq import Groq
from openai import OpenAI
from anthropic import Anthropic
from mistralai import Mistral

# Ambil Token dan API Key secara aman dari Environment Variables server
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Inisialisasi Bot & Client AI
bot = telebot.TeleBot(TELEGRAM_TOKEN)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# Handler /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    nama = message.from_user.first_name
    bot.reply_to(message, f"Halo {nama}! 🚀 Bot `duero_bot` aktif dan didukung oleh jajaran AI terbaik dunia (Gemini, Llama, ChatGPT, Claude, & Mistral). Silakan kirim pesan atau tanyakan apa saja!")

# Handler Pesan Masuk (Sistem Rantai Multi-AI / Fallback)
@bot.message_handler(func=lambda message: True)
def handle_all_ai(message):
    user_text = message.text
    chat_id = message.chat.id
    
    bot.send_chat_action(chat_id, 'typing')
    
    teks_jawaban = ""
    respon_berhasil = False

    # --- 1. GOOGLE GEMINI ---
    if not respon_berhasil:
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_text,
            )
            teks_jawaban = response.text + "\n\n*(🧠 Powered by Google Gemini)*"
            respon_berhasil = True
        except Exception as e:
            print(f"Gemini error: {e}, lanjut ke AI berikutnya...")

    # --- 2. GROQ (LLAMA) ---
    if not respon_berhasil:
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_text}]
            )
            teks_jawaban = response.choices[0].message.content + "\n\n*(⚡ Powered by Groq Llama)*"
            respon_berhasil = True
        except Exception as e:
            print(f"Groq error: {e}, lanjut ke AI berikutnya...")

    # --- 3. OPENAI (GPT) ---
    if not respon_berhasil:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_text}]
            )
            teks_jawaban = response.choices[0].message.content + "\n\n*(🤖 Powered by OpenAI GPT)*"
            respon_berhasil = True
        except Exception as e:
            print(f"OpenAI error: {e}, lanjut ke AI berikutnya...")

    # --- 4. ANTHROPIC (CLAUDE) ---
    if not respon_berhasil:
        try:
            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1000,
                messages=[{"role": "user", "content": user_text}]
            )
            teks_jawaban = response.content[0].text + "\n\n*(🔮 Powered by Anthropic Claude)*"
            respon_berhasil = True
        except Exception as e:
            print(f"Claude error: {e}, lanjut ke AI terakhir...")

    # --- 5. MISTRAL AI ---
    if not respon_berhasil:
        try:
            response = mistral_client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": user_text}]
            )
            teks_jawaban = response.choices[0].message.content + "\n\n*(🌊 Powered by Mistral AI)*"
            respon_berhasil = True
        except Exception as e:
            print(f"Mistral error: {e}")

    # Kirim hasil ke Telegram
    if respon_berhasil:
        bot.reply_to(message, teks_jawaban)
    else:
        bot.reply_to(message, "Waduh, semua server AI sedang sibuk atau mengalami kendala. Coba beberapa saat lagi ya, bro!")

# Jalankan Bot
print("Bot duero_bot All-In-One Multi-AI berhasil dijalankan!")
bot.infinity_polling()
