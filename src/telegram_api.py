import json
import requests
import os
import time

TOKEN = ""
PORT = 0
try:
    TOKEN = os.environ["TOKEN"]
    PORT = os.environ["PORT"]
except KeyError:
    print("Sem variáveis de ambiente TOKEN e PORT!")

API_URL = "https://api.telegram.org/" + TOKEN + "/"

WEBHOOK_URL = "https://the-bobobot.herokuapp.com/" + TOKEN


def get_api(method, param):
    rValue = requests.get(url=API_URL + method, params=param)
    return rValue


def post_api(method, param):
    rValue = requests.post(url=API_URL + method, params=param)
    return rValue


def start_webhook():
    method = "setWebhook"
    param = {"url": WEBHOOK_URL}
    keep_trying = True
    while keep_trying:
        response = post_api(method,param).json()
        if response["ok"]:
            keep_trying = False
        else:
            time.sleep(10)


def send_animation(param):
    return post_api("sendAnimation", param)


def send_document(param):
    return post_api("sendDocument", param)


def send_video(param):
    return post_api("sendVideo", param)


def send_photo(param):
    return post_api("sendPhoto", param)


def send_sticker(param):
    return post_api("sendSticker", param)


def send_message(param):
    return post_api("sendMessage", param)


def send_poll(param):
    return post_api("sendPoll", param)


class Message:
    def __init__(self, message):
        self.message = message

    def get_message_animation(self):
        if "animation" in self.message:
            return self.message["animation"]["file_id"]
        else:
            return ""

    def get_message_sticker(self):
        if "sticker" in self.message:
            return self.message["sticker"]["file_id"]
        else:
            return ""

    def get_message_document(self):
        if "document" in self.message:
            return self.message["document"]["file_id"]
        else:
            return ""

    def get_message_video(self):
        if "video" in self.message:
            return self.message["video"]["file_id"]
        else:
            return ""

    def get_message_photo(self):
        if "photo" in self.message:
            return self.message["photo"][0]["file_id"]
        else:
            return ""

    def get_message_caption(self):
        if "caption" in self.message:
            return self.message["caption"]
        else:
            return ""

    def get_message_id(self):
        if "message_id" in self.message:
            return self.message["message_id"]
        return -1

    def get_chat_id(self):
        return self.message["chat"]["id"]

    def get_sender_id(self):
        return self.message["from"]["id"]

    def get_sender_username(self):
        if "username" in self.message["from"]:
            return self.message["from"]["username"]
        return ""

    def get_sender_first_name(self):
        if "first_name" in self.message["from"]:
            return self.message["from"]["first_name"]
        else:
            return "ERROR: NO FIRST NAME FOUND"

    def get_message_text(self):
        if "text" in self.message:
            return self.message["text"]
        return "ERROR: NO TEXT FOUND"

    def reply(self, replyText, replyMessage=True, private=False):
        replyMessageId = 0
        chatId = self.get_chat_id()
        if private:
            chatId = self.get_sender_id()
        if replyMessage:
            replyMessageId = self.get_message_id()
        param = {"text": replyText,
                 "reply_to_message_id": replyMessageId,
                 "chat_id": chatId}
        return send_message(param)

    def delete(self):
        param = {"chat_id": self.get_chat_id(),
                 "message_id": self.get_message_id()}
        post_api("deleteMessage", param)
