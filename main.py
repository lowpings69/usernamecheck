import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Load environment variables


client = OpenAI(api_key="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")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token("8789745126:AAGJvxxFVlrmUucz6TJrh04HQNPQkb-oFqM").build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
