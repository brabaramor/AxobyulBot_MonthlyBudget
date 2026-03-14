from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
 
# Estados da conversa
MENU = 1
WAITING_DATA = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Oie, eu sou o Axobyul ᓬ(•ᴗ•)ᕒ, o que você quer fazer?\n\n"
        "1 para consultar quanto você ainda tem\n"
        "2 para registrar uma nova compra"
    )
    return MENU

async def receive_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    option = update.message.text.strip()

    if option == "1":
        await update.message.reply_text("Ainda tô aprendendo a fazer isso ᓬ(••')ᕒ")
        return MENU
    elif option == "2":
        await update.message.reply_text(
            "Digite os dados nesta ordem, separados por vírgula:\n\n"
            "O que, Valor total, Valor da parcela, Quantidade de parcelas, Categoria, Subcategoria, dd/mm/aa\n\n"
            "Exemplo ᓬ(•ᴗ•)ᕒ:\n"
            "Amazon Tonico facial etc, 300, 100, 3, Skincare/Haircare, Parceladas, 10/03/26"
        )
        return WAITING_DATA
    else:
        await update.message.reply_text("Que opção é essa? ᓬ(•-•)ᕒ")
        return MENU