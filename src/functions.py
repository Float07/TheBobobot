import database_handler
import reddit_api as reddit
import telegram_api as telegram
import strings_data as str_data
import json
import time
import os
from flask import Flask, request, Response


#Subreddits suportados
SUPPORTED_SUBREDDITS = ["blursedimages",
                        "aww",
                        "memes",
                        "wholesomememes",
                        "eyebleach",
                        "programmerhumor"]

#Configuração spotteds
SPOTTED_LIST = []
MAX_SPOTTED_TIME = 180

#If True will print messages objecs
DEBUG_TOGGLE = False


def start_bot():
    telegram.start_webhook()


def process_message(request):
    oMessage = telegram.Message(request)
    message = oMessage.message

    #prints if debug is toggled on
    if DEBUG_TOGGLE:
        print(message)

    if "text" in message:
        messageSplit = (message["text"]).split(' ', 1)
        command = (messageSplit[0]).split('@', 1)
        if command[0] in textCommandsList:
            (textCommandsList[command[0]])(oMessage)
        elif oMessage.get_chat_id() in blacklisted:
            param = {"chat_id": main_group_id,
                    "text": oMessage.get_message_text()}
            telegram.send_message(param)
    elif "photo" in message:
        if "caption" in message:
            captionSplit = (message["caption"]).split(' ', 1)
            command = (captionSplit[0]).split('@', 1)
            if command[0] in photoCommandsList:
                (photoCommandsList[command[0]])(oMessage)
            elif oMessage.get_chat_id() in blacklisted:
                param = {"chat_id": main_group_id,
                        "caption": oMessage.get_message_caption(),
                        "photo": oMessage.get_message_photo()}
                telegram.send_photo(param)
    elif "animation" in message:
        send_anon_gif(oMessage)
    elif "video" in message:
        if "caption" in message:
            captionSplit = (message["caption"]).split(' ',1)
            command = (captionSplit[0]).split('@',1)
            if command[0] in videoCommandsList:
                (videoCommandsList[command[0]])(oMessage)
    elif "sticker" in message:
        send_anon_sticker(oMessage)
    elif "document" in message:
        send_anon_document(oMessage)
    return Response(status=200)
        


def feat_help(oMessage):
    message_split = oMessage.get_message_text().split(' ', 1)
    help_message = ""
    group_id = oMessage.get_chat_id()
    language = database_handler.get_group_language(group_id)
    if len(message_split) <= 1:
        help_message = "help"
    else:
        help_message = message_split[1]
    param = {"chat_id": group_id,
            "text": str_data.get_string([language, "help", help_message]),
            "parse_mode": "HTML"}
    return telegram.send_message(param)


def toggle_debug(oMessage):
    global DEBUG_TOGGLE
    DEBUG_TOGGLE = not DEBUG_TOGGLE
    if DEBUG_TOGGLE:
        print("Debug now on!")
    else:
        print("debug now off!")


def send_anon_document(oMessage):
    group_id = database_handler.get_registered_user(oMessage.get_chat_id())
    if group_id != None:
        param = {"chat_id": group_id,
                "document": oMessage.get_message_document(),
                "caption": "Documento anônimo. Yaarrr!"}
        telegram.send_document(param)


def send_anon_sticker(oMessage):
    group_id = database_handler.get_registered_user(oMessage.get_chat_id())
    if group_id != None:
        param = {"chat_id": group_id,
                 "sticker": oMessage.get_message_sticker()}
        telegram.send_sticker(param)


def send_anon_video(oMessage, startCaption = "<b>Vídeo anônimo</b>: "):
    group_id = database_handler.get_registered_user(oMessage.get_sender_id())
    if group_id != None:
        captionSplit = oMessage.get_message_caption().split(' ', 1)
        caption = " "
        if len(captionSplit) > 1:
            caption = captionSplit[1]
        param = {"chat_id": group_id,
                 "video": oMessage.get_message_video(),
                 "caption": startCaption + caption,
                 "parse_mode": "HTML"}
        return telegram.send_video(param)
    else:
        oMessage.reply("Você não está registrado, bobão! Registre usando /register.")
        return {}


def send_anon_gif(oMessage):
    group_id = database_handler.get_registered_user(oMessage.get_chat_id())
    if group_id != None:
        param = {"chat_id": group_id,
                 "animation": oMessage.get_message_animation(),
                 "caption": "GIF anônimo!"}
        telegram.send_animation(param)


def send_anon_image(oMessage, startCaption = "<b>Mensagem anônima</b>: "):
    group_id = database_handler.get_registered_user(oMessage.get_sender_id())
    if group_id != None:
        captionSplit = oMessage.get_message_caption().split(' ', 1)
        caption = " "
        if len(captionSplit) > 1:
            caption = captionSplit[1]
        param = {"chat_id": group_id,
                 "photo": oMessage.get_message_photo(),
                 "caption": startCaption + caption,
                 "parse_mode": "HTML"}
        return telegram.send_photo(param)
    else:
        oMessage.reply("Você não está registrado, bobão! Registre usando /register.")
        return {}


def send_anon_text(oMessage, startingText = "<b>Mensagem anônima</b>: "):
    group_id = database_handler.get_registered_user(oMessage.get_sender_id())
    if group_id != None:
        messageSplit = oMessage.get_message_text().split(' ', 1)
        if len(messageSplit) > 1:
            param = {"chat_id": group_id,
                     "text": startingText + messageSplit[1],
                     "parse_mode": "HTML"}
            return telegram.send_message(param)
        else:
            return {}
    else:
        oMessage.reply("Você ainda não está registrado. Use /register para se registrar.")
        return {}


def register_user(oMessage):
    database_handler.set_user_group(oMessage.get_sender_id(), oMessage.get_chat_id())
    oMessage.reply("Você foi registrado! Não envie coisas de otako. :)", False, True)
    oMessage.delete()


def explode(oMessage):
    oMessage.reply("BOOOOOOOOOOOOOOOOoooooOOoOOOooom!💥", True)


def start_ban_poll(oMessage):
    splitMessage = oMessage.get_message_text().split(' ', 1)
    banned = "Meireles"
    if len(splitMessage) > 1:
        banned = splitMessage[1]

    question = "Devemos banir " + banned + "?"
    options = json.dumps(["Sim", "Não", "Ban Meireles"])

    param = {"chat_id": oMessage.get_chat_id(),
             "question": question,
             "options": options,
             "is_anonymous": False}
    telegram.send_poll(param)


def reddit_random_submission(oMessage):
    splitMessage = oMessage.get_message_text().split(' ', 1)

    if len(splitMessage) == 1:
        message = "Utilize '/reddit <Nome do Subreddit>' para pedir por um post aleatório de um subreddit" \
                  "Exemplos:"
        for sub in SUPPORTED_SUBREDDITS:
            message = message + "\n-" + "/reddit " + sub
        oMessage.reply(message)
    else:
        try:
            submission = reddit.get_random_submission(splitMessage[1])
            if not submission.over_18 or oMessage.get_chat_id() == -466715742:
                param = {"chat_id": oMessage.get_chat_id(),
                        "photo": submission.url,
                        "parse_mode": "html",
                        "caption": "<b>" + submission.title + "</b>    " + \
                                    "\n🔼:" + str(submission.score) + " 💬:" + str(submission.num_comments) \
                                    + " 🔼/🔽:" + str(
                            submission.upvote_ratio * 100) + "%" "\nreddit.com" + submission.permalink}
                telegram.send_photo(param)
            else:
                oMessage.reply("Vish. Peguei um post NSFW. Melhor não mandar :(")
        except:
            oMessage.reply("Algo deu errado. Mas não sei oque é. Foi mal :)\nTalves esse subereddit não exista?")
            return

def get_spotted_message_by_message_id(messageId):
    for spottedUser in SPOTTED_LIST:
        if spottedUser["message_id"] == messageId:
            return spottedUser
    return {}


def finish_spotted(index = 0):
    finishedSpottedMessage = SPOTTED_LIST[0]
    text = "Votação encerrada! Resultados:\n"
    mostVoted = ""
    for key in finishedSpottedMessage["voting"]["votes"]:
        if key.isnumeric():
            text = text + '<a href="tg://user?id=' + key + '">Essa pessoa sem username</a>: '
        else:
            text = text + "@" + key + ": "
        votes = finishedSpottedMessage["voting"]["votes"][key]
        text = text + str(votes) + "\n"
        if mostVoted not in finishedSpottedMessage["voting"]["votes"] or votes > finishedSpottedMessage["voting"]["votes"][mostVoted]:
            mostVoted = key
    text = text + "Votos totais: " + str(finishedSpottedMessage["voting"]["amount"]) + "\n"

    if (mostVoted == finishedSpottedMessage["username"] and mostVoted != "") or mostVoted == str(finishedSpottedMessage["user_id"]):
        text = text + "Parabéns! Vocês acertaram. O usuário que enviou foi "
        if finishedSpottedMessage["username"] == "":
            text = text + '<a href="tg://user?id=' + mostVoted + '">' + finishedSpottedMessage["first_name"] + '.</a>!'
        else:
            text = text + "@" + finishedSpottedMessage["username"] + "!"
    else:
        text = text + "A pessoa mais votada foi "
        if mostVoted.isnumeric():
            text = text + '<a href="tg://user?id=' + mostVoted + '">essa pessoa sem username.</a>'
        else:
            text = text + "@" + mostVoted
        text = text + ". Mas ela não enviou o spotted. A pessoa que enviou continua anônima :("

    chatId = finishedSpottedMessage["chat_id"]
    parseMode = "HTML"
    replyId = finishedSpottedMessage["message_id"]
    param = {"text": text,
             "chat_id": chatId,
             "parse_mode": parseMode,
             "reply_to_message_id": replyId}
    if mostVoted != "":
        telegram.send_message(param)
    SPOTTED_LIST.pop(0)


def spotted_update():
    if len(SPOTTED_LIST) == 0:
        return

    currentTime = time.clock_gettime(time.CLOCK_MONOTONIC)
    if currentTime - SPOTTED_LIST[0]["time_sent"] > MAX_SPOTTED_TIME:
        finish_spotted()


def add_spotted_user(spottedUser):
    SPOTTED_LIST.append(spottedUser)


def spotted_send_message(oMessage):
    spottedMessage = {
        "first_name": oMessage.get_sender_first_name(),
        "username": oMessage.get_sender_username(),
        "user_id": oMessage.get_sender_id(),
        "time_sent": time.clock_gettime(time.CLOCK_MONOTONIC),
        "voting": {
            "voted": [],
            "amount": 0,
            "votes": {}
        }
    }
    response = send_anon_text(oMessage, "<b>Texto spotted</b>: ")
    if not bool(response):
        return
    messageSent = response.json()["result"]
    spottedMessage["message_id"] = messageSent["message_id"]
    spottedMessage["chat_id"] = messageSent["chat"]["id"]
    add_spotted_user(spottedMessage)


def spotted_send_image(oMessage):
    spottedMessage = {
        "first_name": oMessage.get_sender_first_name(),
        "username": oMessage.get_sender_username(),
        "user_id": oMessage.get_sender_id(),
        "time_sent": time.clock_gettime(time.CLOCK_MONOTONIC),
        "voting": {
            "voted": [],
            "amount": 0,
            "votes": {}
        }
    }
    response = send_anon_image(oMessage, "<b>Imagem spotted</b>: ")
    if not bool(response):
        return
    messageSent = response.json()["result"]
    spottedMessage["message_id"] = messageSent["message_id"]
    spottedMessage["chat_id"] = messageSent["chat"]["id"]
    add_spotted_user(spottedMessage)


def spotted_send_video(oMessage):
    spottedMessage = {
        "first_name": oMessage.get_sender_first_name(),
        "username": oMessage.get_sender_username(),
        "user_id": oMessage.get_sender_id(),
        "time_sent": time.clock_gettime(time.CLOCK_MONOTONIC),
        "voting": {
            "voted": [],
            "amount": 0,
            "votes": {}
        }
    }
    response = send_anon_video(oMessage, "<b>Video spotted</b>: ")
    if not bool(response):
        return
    messageSent = response.json()["result"]
    spottedMessage["message_id"] = messageSent["message_id"]
    spottedMessage["chat_id"] = messageSent["chat"]["id"]
    add_spotted_user(spottedMessage)


def spotted_vote(oMessage):
    message = oMessage.message
    if "reply_to_message" not in message:
        oMessage.reply("Responda à mensagem que você queira votar. Bobo.", True, True)
        oMessage.delete()
        return
    if len(message["entities"]) <= 1:
        oMessage.reply("Responda da forma '/spottedvote @usuário.'", True, True)
        oMessage.delete()
        return
    votedId = message["reply_to_message"]["message_id"]
    spottedMessageVoted = get_spotted_message_by_message_id(votedId)
    if not bool(spottedMessageVoted):
        oMessage.reply("Essa mensagem não é um spotted :(", True, True)
        oMessage.delete()
        return
    if oMessage.get_sender_id() in spottedMessageVoted["voting"]["voted"]:
        oMessage.reply("Você já votou!! >:(", True, True)
        oMessage.delete()
        return

    if message["entities"][1]["type"] == "mention":
        username = message["text"][message["entities"][1]["offset"] + 1: message["entities"][1]["offset"] + message["entities"][1]["length"]]
        if username in spottedMessageVoted["voting"]["votes"]:
            spottedMessageVoted["voting"]["votes"][username] = spottedMessageVoted["voting"]["votes"][username] + 1
        else:
            spottedMessageVoted["voting"]["votes"][username] = 1
    elif message["entities"][1]["type"] == "text_mention":
        userId = str(message["entities"][1]["user"]["id"])
        if userId in spottedMessageVoted["voting"]["votes"]:
            spottedMessageVoted["voting"]["votes"][userId] = spottedMessageVoted["voting"]["votes"][userId] + 1
        else:
            spottedMessageVoted["voting"]["votes"][userId] = 1
    else:
        oMessage.reply("Você precisa marcar alguem. Por exemplo, '/spottedvote @andrezão'.")
        return
    spottedMessageVoted["voting"]["voted"].append(oMessage.get_sender_id())
    spottedMessageVoted["voting"]["amount"] = spottedMessageVoted["voting"]["amount"] + 1

def response_pong(oMessage):
    oMessage.reply("Pong")


#Configuração para os comandos
main_group_id = -1001367341107
blacklisted = [1080820184, 735844467]
textCommandsList = {"/explode": explode,
                    "/anon": send_anon_text,
                    "/register": register_user,
                    "/ban": start_ban_poll,
                    "/reddit": reddit_random_submission,
                    "/spotted": spotted_send_message,
                    "/svote": spotted_vote,
                    "/ping": response_pong,
                    "/help": feat_help,
                    "/debugtgl": toggle_debug}
photoCommandsList = {"/anon": send_anon_image,
                    "/spotted": spotted_send_image}
videoCommandsList = {"/anon": send_anon_video,
                    "/spotted": spotted_send_video}

