"""Module to define telegram Bot related classes and functions."""

import sys
import json
import requests
from framex_dev import Video

BASE_URL = 'https://framex-dev.wadrid.net/api/video/'\
           'Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c'

def get_token():
    """Token for Telegram Bot."""
    with open('token.json') as json_file:
        return json.load(json_file)['token']

class BotHandler:
    """Manages Telegram Bot interaction."""

    def __init__(self, token):
        """Necessary variables for Bot interaction.

        api_url is the specific url using the token
        """
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=30):
        """Bot refresh from API."""
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + 'getUpdates', params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text, repkboard=False):
        """Render text reply to chat."""
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        if repkboard:
            keyboard_buttons = ['Yes', 'No', 'Exit']
            keyboard_buttons = [{'text': x} for x in keyboard_buttons]
            rep_keyb_mkup = {'keyboard': [keyboard_buttons],
                                   'resize_keyboard': True}
            params['reply_markup'] = json.dumps(rep_keyb_mkup)
        else:
            rep_keyb_rem = {'remove_keyboard': True}
            params['reply_markup'] = json.dumps(rep_keyb_rem)


        resp = requests.post(self.api_url + 'sendMessage', params)
        return resp

    def send_photo(self, chat_id, photo):
        """Render image reply to chat."""
        params = {'chat_id': chat_id, 'photo': photo, 'parse_mode': 'HTML'}
        resp = requests.post(self.api_url + 'sendPhoto', params)
        return resp


magnito_bot = BotHandler(get_token()) #Your bot's name


def main():
    """Server process to manage bot interaction.

    All calls to telegram API are done with the BotHandler class
    User interaction is taken care of in this function
    """

    def get_message(update):
        """Message from update data."""
        if update.get('message'):
            return update.get('message')
        return update.get('edited_message')

    def get_first_name(message):
        """First name from message data."""
        first_name = 'unknown'
        if 'first_name' in message['chat']:
            first_name = message['chat']['first_name']
        elif 'new_chat_member' in message:
            first_name = message['new_chat_member']['username']
        elif 'from' in message:
            first_name = message['from']['first_name']
        return first_name

    def get_user_response(message):
        """User response from message."""
        if 'text' in message:
            return message['text'].lower()
        return 'New member'

    new_offset = 0
    rocket_finished = True
    print('hi, now launching...')

    while True:
        for update in magnito_bot.get_updates(new_offset):
            print(update)

            # Getting Data from update
            update_id = update.get('update_id')
            message = get_message(update)
            chat_id = message['chat']['id']
            first_name = get_first_name(message)
            user_response = get_user_response(message)

            # Initiating objects if no game is already started.
            # This is only carried out at the begining of each game
            if rocket_finished:
                if user_response == '/rocket':
                    rocket_finished = False
                    vid = Video(BASE_URL)
                    output_text = 'Rocket bot initiated'
                else:
                    output_text = 'How are you doing {}'.format(first_name)
                magnito_bot.send_message(chat_id, output_text)

            if not rocket_finished:
                if user_response == 'yes':
                    vid.remove('gt')
                elif user_response == 'no':
                    vid.remove('lte')

                if user_response == 'exit':
                    rocket_finished = True
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
        sys.exit()
