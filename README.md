[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/notpixel/app?startapp=f1197825376)

#  AUTO FARM FOR NotPixel 🚀
![start](https://github.com/user-attachments/assets/3467f0e3-44ac-4a19-8fc0-878bf9ad364a)

# 🔥🔥 PYTHON version must be 3.10 🔥🔥

> 🇷 🇺 README in russian available [here](README-RU.md)

## Features  
|                      Feature                       | Supported |
|:--------------------------------------------------:|:---------:|
|                   Multithreading                   |     ✔️    |
|              Proxy binding to session              |     ✔️    |
|         User-Agent binding to session              |     ✔️    |
| Auto-register your account with your referral link |     ✔️    |
|                  Daily rewards                     |     ✔️    |
|                     Auto tasks                     |     ✔️    |
|           Support for pyrogram .session            |     ✔️    |



## [Settings]
| Settings                |                                 Description                                 |
|-------------------------|:---------------------------------------------------------------------------:|
| **API_ID / API_HASH**   | Platform data from which to run the Telegram session (by default - android) |
| **SLEEP_TIME**          |           Sleep time between cycles (by default - [2700, 4200])             |
| **START_DELAY**         |            Delay between sessions at start (by default - [5, 100)           |
| **AUTO_DRAW**           |                    Auto-drawing pixels (default - True)                     |
| **AUTO_UPGRADE**        |              Auto-upgrading your mining stuff (default - True)              |
| **CLAIM_REWARD**        |                     Claim daily reward (default - True)                     |
| **AUTO_TASK**           |                     Auto tasks (default - True)                             |
| **TASKS_TO_DO**         |              List of tasks for auto-task (default - all tasks)              |
| **REF_ID**              |   Your referral argument (comes after app/startapp? in your referral link)  |

## Quick Start 📚

To fast install libraries and run bot - open `run.bat` on **Windows** or `run.sh` on **Linux**

## Prerequisites
Before you begin, make sure you have the following installed:
- [**Python**](https://www.python.org/downloads/release/python-3100/) **version 3.10**

## Obtaining API Keys
1. Go to [**my.telegram.org**](https://my.telegram.org/auth) and log in using your phone number.
2. Select `API development tools` and fill out the form to register a new application.
3. Record the `API_ID` and `API_HASH` provided after registering your application in the `.env` file.

## Installation
You can download the [**repository**](https://github.com/BlackJkee/NotPixelBot) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/BlackJkee/NotPixelBot.git
cd NotPixelBot
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/NotPixelBot >>> python3 main.py --action (1/2)
# Or
~/NotPixelBot >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```
You can also use arguments for quick start, for example:
```shell
~/NotPixelBot >>> python main.py --action (1/2)
# Or
~/NotPixelBot >>> python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

### Usages
When you first launch the bot, create a session for it using the `Creates a session` command. It will create a `sessions` folder in which all accounts will be stored, as well as a file `accounts.json` with configurations.
If you already have sessions, simply place them in a folder `sessions` and run the clicker. During the startup process you will be able to configure the use of a proxy for each session.
User-Agent is created automatically for each account.

Here is an example of what `accounts.json` should look like:
```shell
[
  {
    "session_name": "name_example",
    "user_agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36",
    "proxy": "type://user:pass:ip:port"  # "proxy": "" - if you dont use proxy
  }
]
```

**v0.1 based on rep - vadymfedorets**
