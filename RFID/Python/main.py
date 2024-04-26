from fastapi import FastAPI, HTTPException
import uvicorn
from pyngrok import ngrok
from classes import FirebaseDB 
import firebase_setup as firedb
import requests
from telegram__bot_setup import TELEGRAM_TOKEN

app = FastAPI()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.post("/register_rfid/")
async def register_rfid(chat_id: int, rfid: str):
    try:
        # Регистрация RFID в базе данных Firebase
        response = requests.put(f"{https_url}/rfid_data/{rfid}.json", json={"chat_id": chat_id})
        response.raise_for_status()

        # Отправка уведомления в Telegram
        message = f"RFID {rfid} зарегистрирован"
        response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": message})
        response.raise_for_status()

        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    firebase_db = FirebaseDB(None, None)
    firebase_db.admin, firebase_db.app = firedb.initialize_connection()

    https_tunnel = ngrok.connect(5080)

    tunnels = ngrok.get_tunnels()

    for tunnel in tunnels:
        if tunnel.proto == "https":
            https_url = tunnel.public_url
            https_url = https_url.split("//")[1]
            ref = firebase_db.admin.reference('/credentials/url')
            ref.set(https_url)
            break

    firedb.drop_connection(firebase_db.app)
    uvicorn.run(app, host="127.0.0.1", port=5080)
