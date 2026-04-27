import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "TELEGRAM_TOKEN"
AI_KEY = "API_KEY"

def ask_ai(text):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {AI_KEY}"},
        json={
            "model": "gpt-4.1",
            "messages": [
                {"role": "system", "content": "Ты эксперт по безопасности VIP."},
                {"role": "user", "content": text}
            ]
        }
    )
    return r.json()["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен. Напиши /risk Москва")

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Напиши: /risk Москва центр")
        return

    result = ask_ai(f"Оцени риск: {text}")
    await update.message.reply_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("risk", risk))

app.run_polling()
