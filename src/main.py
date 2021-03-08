import telegram_api as telegram
import functions as fn
import time
import threading
from flask import Flask, request, Response
import os

TOKEN = ""
PORT = 0
try:
    TOKEN = os.environ["TOKEN"]
    PORT = os.environ["PORT"]
except KeyError:
    print("Sem variáveis de ambiente TOKEN e PORT!")


def main():

    fn.start_bot()
    
    keepGoing = True
    while keepGoing:
        fn.spotted_update()
        time.sleep(2)


def start_flask_app():
    app = Flask(__name__)
    @app.route("/")
    def respond():
        return("Oi tudo bom? :3")
    @app.route("/" + TOKEN,methods=["POST", "GET"])
    def respond_API():
        update_json = request.json
        if "message" in update_json:
            fn.process_message(update_json["message"])
            return "ok"
        return "Ué vc n é a API do Telegram. SAI DAQUI VEEEEEEI"
    app.run(host='0.0.0.0', port=PORT)


if __name__ == "__main__":
    app_thread = threading.Thread(target=start_flask_app)
    app_thread.start()
    main()
