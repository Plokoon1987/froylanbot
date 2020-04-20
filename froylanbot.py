# -*- coding: UTF8 -*-
from urllib import parse
import requests
import datetime
import json

def get_token():
    with open('token.json') as json_file:
        return json.load(json_file)['token']

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update

token = get_token() #Token of your bot
magnito_bot = BotHandler(token) #Your bot's name


def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        for update in magnito_bot.get_updates(new_offset):
            print(update)
            update_id = update['update_id']
            chat_id = update['message']['chat']['id']

            text='New member'
            if 'text' in update['message']:
                text = update['message']['text']


            if 'first_name' in update['message']:
                first_chat_name = update['message']['chat']['first_name']
            elif 'new_chat_member' in update['message']:
                first_chat_name = update['message']['new_chat_member']['username']
            elif 'from' in update['message']:
                first_chat_name = update['message']['from']['first_name']
            else:
                first_chat_name = "unknown"

            if text == 'Hi':
                magnito_bot.send_message(chat_id, 'Morning ' + first_chat_name)
                new_offset = update_id + 1
            else:
                magnito_bot.send_message(chat_id, 'How are you doing '+first_chat_name)
                new_offset = update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
