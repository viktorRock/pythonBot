import json 
import requests
import os
import urllib
import time
import sys

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    if sys.version_info[0] < 3:
        text = urllib.quote_plus(text)
    else:
        text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def sendDefErrorMsg(update):
    chat = update["message"]["chat"]["id"]
    text = "Por enquanto consigo responder somente texto :)"
    send_message(text, chat)

def echo_all(updates):
    for update in updates["result"]:
        if "message" in update:
            message = update["message"]
        elif "edited_message" in update:
            message = update["edited_message"]

        if "text" in message:
            text = message["text"]
            chat = message["chat"]["id"]
            send_message(text, chat)
        else:
            sendDefErrorMsg(update)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()