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

Type '/rocket' in the Telegram app to start the "rocket" program

## Files
* framex_dev.py: Module to define Video related classes and functions
* froylanbot.py: Module to define telegram Bot related classes and functions

* token.json: File containing the telebram bot token
* restart.sh: Script to initialize a virtualenv with all the needed requirements. python3-venv needs to be installed to be able to use it
