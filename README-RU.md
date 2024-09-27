[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/Binance_Moonbix_bot/start?startApp=ref_1197825376&startapp=ref_1197825376&utm_medium=web_share_copy)

# АВТО ФАРМ ДЛЯ BinanceNotPixelBot🚀



# 🔥🔥 Используйте PYTHON версии 3.10 🔥🔥

> 🇪🇳 README in english available [here](README-EN)

## Функционал  
|                   Функционал                   | Поддерживается |
|:----------------------------------------------:|:--------------:|
|                Многопоточность                 |       ✔️       | 
|            Привязка прокси к сессии            |       ✔️       |
|          Привязка User-Agent к сессии          |       ✔️       | 
| Авто-регистрация аккаунта по вашей реф. ссылке |       ✔️       |
|               Ежедневные награды               |       ✔️       |
|                   Авто таски                   |       ✔️       |
|          Поддержка pyrogram .session           |       ✔️       |


## [Настройки](https://github.com/BlackJkee/NotPixelBot/blob/main/.env-example/)
|       Настройки         |                              Описание                                               |
|-------------------------|:-----------------------------------------------------------------------------------:|
| **API_ID / API_HASH**   | Данные платформы, с которой будет запущена сессия Telegram (по умолчанию - android) |
| **SLEEP_TIME**          |           Время сна между циклами (по умолчанию - [2700, 4200])                     |
| **START_DELAY**         |            Задержка между сеансами при запуске (по умолчанию - [5, 100])            |
| **AUTO_DRAW**           |            Автоматическая прорисовка пикселей (по умолчанию - True)                 |
| **AUTO_UPGRADE**        |       Автоматическое обновление материалов для майнинга (по умолчанию - True)       |
| **CLAIM_REWARD**        |              Собирать ежедневное вознаграждение (по умолчанию - True)               |
| **AUTO_TASK**           |                Автоматические задания (по умолчанию - True)                         |
| **TASKS_TO_DO**         |          Список задач для автозадачи (по умолчанию - все задачи)                    |
| **REF_ID**              |   Ваш реферальный аргумент (идет после app/startapp? в вашей реф. ссылке)           |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл `run.bat` на **Windows** или `run.sh` на **Линукс**

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/release/python-3100/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [**my.telegram.org**](https://my.telegram.org/auth) и войдите в систему, используя свой номер телефона.
2. Выберите `API development tools` и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/BlackJkee/NotPixelBot) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/BlackJkee/NotPixelBot.git
cd NotPixelBot
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/NotPixelBot >>> python3 main.py --action (1/2)
# Or
~/NotPixelBot >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/NotPixelBot >>> python main.py --action (1/2)
# Или
~/NotPixelBot >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```

### Usages
Когда вы впервые запустите бота, создайте для него сессию с помощью команды `Creates a session`. При этом будет создана папка `sessions`, в которой будут храниться все аккаунты, а также файл `accounts.json` с конфигурациями.
Если у вас уже есть сессии, просто поместите их в папку `sessions` и запустите кликер. В процессе запуска вы сможете настроить использование прокси для каждой сессии.
User-Agent создается автоматически для каждой учетной записи.

Вот пример того, как должен выглядеть файл `accounts.json`:
```shell
[
  {
    "session_name": "name_example",
    "user_agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36",
    "proxy": "type://user:pass:ip:port"  # "proxy": "" - if you dont use proxy
  }
]
```

**v0.1 создано на основе репы - vadymfedorets**
