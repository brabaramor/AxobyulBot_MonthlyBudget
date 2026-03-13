from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers.menu import start, receive_option, MENU
from handlers.record import receive_data, WAITING_DATA
from dotenv import load_dotenv
import os #usado para acessar o env e ler os tokens

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    app = ApplicationBuilder.token(TOKEN).build()
    session = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_option)],
            WAITING_DATA: [MessageHandler(filters.TEXT & -filters.COMMAND, receive_option)]
        },
        fallbacks=[CommandHandler("start",start)],
    )
    app.add_handler(session)
    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()