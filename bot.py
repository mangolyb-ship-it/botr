import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 1514979458

RESPONSES = [
    "Сообщение получено.",
    "Информация принята.",
    "Ваше сообщение обработано."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен. Готов к работе.")
    
    # Уведомляем админа
    user = update.effective_user
    await context.bot.send_message(
        ADMIN_ID,
        f"👤 Пользователь {user.full_name} (ID: {user.id}) запустил бота."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отвечаем пользователю
    reply = random.choice(RESPONSES)
    await update.message.reply_text(reply)
    
    # Отправляем админу
    user = update.effective_user
    message = update.message
    
    # Формируем сообщение для админа
    admin_msg = f"👤 {user.full_name} (ID: {user.id})\n"
    
    if message.text:
        admin_msg += f"💬 {message.text}\n"
    else:
        admin_msg += f"📁 [МЕДИА]\n"
    
    admin_msg += f"🤖 Бот ответил: {reply}"
    
    await context.bot.send_message(ADMIN_ID, admin_msg)
    
    # Пересылаем медиа если есть
    if message.photo or message.video or message.document or message.voice:
        await message.forward(ADMIN_ID)

def main():
    print("🤖 Бот запущен")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == '__main__':

    main()
