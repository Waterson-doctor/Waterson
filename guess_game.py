import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# تحميل المتغيرات من .env
load_dotenv()

# قراءة التوكن
TOKEN = os.getenv('TOKEN')
print(f'Token: {TOKEN}')  # طباعة التوكن للتأكد من أنه تم قراءته بشكل صحيح

# متغير للعدد الذي يجب تخمينه
secret_number = random.randint(1, 100)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في لعبة التخمين! ابدأ بإدخال رقم بين 1 و 100.")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global secret_number
    try:
        user_guess = int(update.message.text)
        if user_guess < secret_number:
            await update.message.reply_text("رقمك أقل من الرقم السري.")
        elif user_guess > secret_number:
            await update.message.reply_text("رقمك أكبر من الرقم السري.")
        else:
            await update.message.reply_text(f"تهانينا! لقد خمّنت الرقم الصحيح: {secret_number}")
            secret_number = random.randint(1, 100)  # إعادة تعيين الرقم السري للعبة جديدة
    except ValueError:
        await update.message.reply_text("يرجى إدخال رقم صحيح.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

    app.run_polling()

if __name__ == '__main__':
    main()
