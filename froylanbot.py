# -*- coding: UTF8 -*-
from urllib import parse
import requests
import datetime
import json
from framex_dev import Video

BASE_URL = 'https://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c'

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

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo, 'parse_mode': 'HTML'}
        method = 'sendPhoto'
        resp = requests.post(self.api_url + method, params)
        return resp


token = get_token() #Token of your bot
magnito_bot = BotHandler(token) #Your bot's name


def main():
    new_offset = 0
    rocket_finished = True
    print('hi, now launching...')

    while True:
        for update in magnito_bot.get_updates(new_offset):
            print(update)
            update_id = update['update_id']
            try:
                message = update['message']
            except:
                message = update['edited_message']
            chat_id = message['chat']['id']

            first_name = "unknown"
            if 'first_name' in message:
                first_name = message['chat']['first_name']
            elif 'new_chat_member' in message:
                first_name = message['new_chat_member']['username']
            elif 'from' in message:
                first_name = message['from']['first_name']

            input_text = 'New member'
            if 'text' in message:
                input_text = message['text']

            if rocket_finished:
                if input_text == '/rocket':
                    rocket_finished = False
                    vid = Video(BASE_URL)
                    output_text = 'Rocket bot initiated'
                    magnito_bot.send_message(chat_id, output_text)
                else:
                    output_text = 'How are you doing {}'.format(first_name)
                    magnito_bot.send_message(chat_id, output_text)

            if not rocket_finished:
                txt = 'endpoints: {}\n\
                       to_bisect: {}\n\
                       {} Did the rocket launch yet?   (Y/n)'
                if not vid.to_bisect():
                    rocket_finished = True
                    output_text = 'Finished!!!'

                elif input_text == '/rocket':
                    index = vid.bisect_frame()
                    output_photo = vid.get_frame(index)
                    output_text = txt.format(str(vid.bisect_endpoints),
                                             str(vid.to_bisect()),
                                             str(index)
                                             )

                elif input_text.lower() == 'y':
                    vid.bisect('below')
                    index = vid.bisect_frame()
                    output_photo = vid.get_frame(index)
                    output_text = txt.format(str(vid.bisect_endpoints),
                                             str(vid.to_bisect()),
                                             str(index)
                                             )

                elif input_text.lower() == 'n':
                    vid.bisect('above')
                    index = vid.bisect_frame()
                    output_photo = vid.get_frame(index)
                    output_text = txt.format(str(vid.bisect_endpoints),
                                             str(vid.to_bisect()),
                                             str(index)
                                             )

                else:
                    output_text = 'That is not a valid answer'

                try:
                    magnito_bot.send_photo(chat_id, output_photo)
                    magnito_bot.send_message(chat_id, output_text)
                except:
                    magnito_bot.send_message(chat_id, output_text)


            new_offset = update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
