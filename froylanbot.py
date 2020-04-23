''' Module to define telegram Bot related classes and functions '''

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

    def send_message(self, chat_id, text, repkboard=False):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        if repkboard:
            keyboard_buttons = ['Yes', 'No', 'Exit']
            keyboard_buttons = [{'text': x} for x in keyboard_buttons]
            ReplyKeyboardMarkup = {'keyboard': [keyboard_buttons],
                                   'resize_keyboard': True}
            params['reply_markup'] = json.dumps(ReplyKeyboardMarkup)
        else:
            ReplyKeyboardRemove = {'remove_keyboard': True}
            params['reply_markup'] = json.dumps(ReplyKeyboardRemove)


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
                if input_text.lower() == 'yes':
                    vid.remove('gte')
                elif input_text.lower() == 'no':
                    vid.remove('lt')

                if input_text.lower() == 'exit':
                    rocket_finished = True
                    output_photo = None
                    output_text = 'Exiting Rocket'
                    magnito_bot.send_message(chat_id, output_text)
                elif vid.can_bisect():
                    output_text = '{} Did the rocket launch yet?'
                    output_photo = vid.get_frame(vid.bisect_frame())
                    output_text = output_text.format(vid.bisect_frame())
                    magnito_bot.send_photo(chat_id, output_photo)
                    magnito_bot.send_message(chat_id, output_text, repkboard=True)
                else:
                    rocket_finished = True
                    output_photo = vid.get_frame(vid.bisect_frame())
                    output_text = 'Finished!!! the launching frame is {}'.format(vid.bisect_frame())
                    magnito_bot.send_photo(chat_id, output_photo)
                    magnito_bot.send_message(chat_id, output_text)

            new_offset = update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
