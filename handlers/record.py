from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from notion_client import Client, APIResponseError
from dotenv import load_dotenv
from handlers.menu import MENU, WAITING_DATA
import json
import os
import uuid
 
load_dotenv()
      
async def receive_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = os.getenv("NOTION_TOKEN").strip()
    DATABASE_ID = os.getenv("NOTION_DATABASE_ID").strip() 
    notion = Client(auth=token)

    receivedText = update.message.text.strip()
    splitedText = [p.strip() for p in receivedText.split(",")]

    if len(splitedText) != 7:
        await update.message.reply_text(
            f"ᓬ(•ᴗ•)ᕒ Recebi {len(splitedText)} campo(s), mas esperava 7.\n"
            "Lembra do formato?\n"
            "Descrição, Valor total, Valor da parcela, Quantidade de parcelas, Categoria, Subcategoria, dd/mm/aa"
        )
        return WAITING_DATA
    
    descricao, valor_total, valor_parcela, qtd_parcelas, categoria, subcategoria, data = splitedText

    try:
        day, month, year = data.split("/")
        if len(year) == 2:
            year = "20" + year
        formatedDate = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except Exception as e:
        await update.message.reply_text(f"Use o formato dd/mm/aa: {(e)}")
        return WAITING_DATA
    
    try:
        valor_total = float(valor_total.replace("R$", "").replace(".", "").replace(",", "."))
        valor_parcela = float(valor_parcela.replace("R$", "").replace(".", "").replace(",", "."))
        qtd_parcelas = int(qtd_parcelas)
    except Exception as e:
        await update.message.reply_text(f"Valores inválidos: {(e)}")
        return WAITING_DATA
    
    recordId = str(uuid.uuid4())[:8].upper()

    payload_properties = {
        "Descrição": {"title": [{"text": {"content": descricao}}]},
        "Valor total": {"number": valor_total},
        "Valor da parcela": {"number": valor_parcela},
        "Qtd parcelas": {"number": qtd_parcelas},

        "Categoria": {"multi_select": [{"name": categoria}]},
        "Subcategoria": {"multi_select": [{"name": subcategoria}]},

        "Data": {"date": {"start": formatedDate}},
        "Id": {"rich_text": [{"text": {"content": recordId}}]},
    }

    print("\n--- DEBUG: DADOS ENVIADOS PARA O NOTION ---")
    print(json.dumps(payload_properties, indent=2, ensure_ascii=False))
    print("-------------------------------------------\n")

    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=payload_properties
        )

        await update.message.reply_text(
            f"✅ Registro salvo!\n\n"
            f"{descricao}\n"
            f"Total: R$ {valor_total:.2f}\n"
            f"Parcela: R$ {valor_parcela:.2f} x {qtd_parcelas}x\n"
            f"{categoria} › {subcategoria}\n"
            f"{data}\n"
            f"{recordId}"
        )    
    except APIResponseError as e:
        print(f"ERRO DA API DO NOTION: {e}")
        await update.message.reply_text(f"ᓬ(••')ᕒ O Notion recusou os dados:\n{e}")
    except Exception as e:
        print(f"ERRO GERAL: {e}")
        await update.message.reply_text(f"ᓬ(••')ᕒ Erro interno: {str(e)}")
    
    return MENU