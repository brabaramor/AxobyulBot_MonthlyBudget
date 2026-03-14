from notion_client import Client

TOKEN_TESTE = "" 

notion = Client(auth=TOKEN_TESTE)

try:
    user = notion.users.me()
    print("✅ SUCESSO! O bot conectou.")
    print(f"Nome do Bot: {user.get('name')}")
except Exception as e:
    print("❌ ERRO CONTINUA:")
    print(e)