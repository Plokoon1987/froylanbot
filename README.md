# froylanbot
Telegram bot to find out a Rocket's launching moment

##  Requirements
python3.5 or above

## Installation
Add a real <telegram_bot_token> token to token.json

Use "requirements.txt" to install the python requirements
```
pip install -r requirements.txt
```

Note: If python3-venv is installed , restart.sh can be used to install the requirements in a virtualenv

## Running the script
Use the following command to run the main script
```
python froylanbot.py
```

Find @Froylanbot in the Telegram App
Type '/rocket' in the chat to start the "rocket" program

## Summary
It was decided to divide the bot in 2 parts: The Video part and the Bot part, as the two of them can be treated independently.

The Video part, "framex_dev.py" takes the url from a Video source. It provides a class "Video" to represent a single Video Source. It also provides functions to be able to determine the rocket's launching moment. It was decided to write this class as generic as possible as it could be reused with other Video Sources

The Bot part, "froylanbot.py" has two main parts to it, The BotHandler class and the main function.

The BotHandler class takes a telegram bot token as an input and it uses it to generate urls to be able to send information to the Client.

The main function uses a combination of both the "Video Class" and the "BotHandler class" to interact with the client in one way or another depending on the client's actions. It is in this function where the Bot's interoperability is defined

Note: The BERNARD framework was not used in this case as I wanted to get a feel of the Telegram Bot API. It was used as a reference for methodology purposes only

## Files
* framex_dev.py: Module to define Video related classes and functions
* froylanbot.py: Module to define telegram Bot related classes and functions

* token.json: File containing the telebram bot token
* restart.sh: Script to initialize a virtualenv with all the needed requirements. python3-venv needs to be installed to be able to use it
