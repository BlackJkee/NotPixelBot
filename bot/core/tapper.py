import asyncio
import base64
import os
import random
from datetime import datetime, timedelta, timezone
from multiprocessing.util import debug
from time import time
from urllib.parse import unquote, quote

import brotli
import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw import types
from pyrogram.raw.functions.messages import RequestAppWebView
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers

from random import randint, choices

from ..utils.file_manager import get_random_cat_image


class Tapper:
    def __init__(self, tg_client: Client):
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.start_param = ''
        self.bot_peer = 'notpixel'

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()

                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)
            peer = await self.tg_client.resolve_peer(self.bot_peer)

            ref = settings.REF_ID
            link = get_link(ref)
            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                platform='android',
                app=types.InputBotAppShortName(bot_id=peer, short_name="app"),
                write_allowed=True,
                start_param=link
            ))

            auth_url = web_view.url

            tg_web_data = unquote(
                string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            tg_web_data_parts = tg_web_data.split('&')

            user_data = tg_web_data_parts[0].split('=')[1]
            chat_instance = tg_web_data_parts[1].split('=')[1]
            chat_type = tg_web_data_parts[2].split('=')[1]
            start_param = tg_web_data_parts[3].split('=')[1]
            auth_date = tg_web_data_parts[4].split('=')[1]
            hash_value = tg_web_data_parts[5].split('=')[1]

            user_data_encoded = quote(user_data)
            self.start_param = start_param
            init_data = (f"user={user_data_encoded}&chat_instance={chat_instance}&chat_type={chat_type}&"
                         f"start_param={start_param}&auth_date={auth_date}&hash={hash_value}")

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return init_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error during Authorization: 😢 <red>{error}</red>")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: aiohttp.ClientSession):
        try:

            response = await http_client.get("https://notpx.app/api/v1/users/me")
            response.raise_for_status()
            response_json = await response.json()
            return response_json

        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error when logging: 😢 <red>{error}</red>")
            logger.warning(f"<blue>{self.session_name}</blue> | Bot overloaded retrying logging in")
            await asyncio.sleep(delay=randint(3, 7))
            await self.login(http_client)

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://ipinfo.io/ip', timeout=aiohttp.ClientTimeout(20))
            ip = (await response.text())
            logger.info(f"<blue>{self.session_name}</blue> | Proxy IP: <light-green>{ip}</light-green>")
        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Proxy: {proxy} | Error: 😢 <red>{error}</red>")

    async def join_tg_channel(self, link: str):
        if not self.tg_client.is_connected:
            try:
                await self.tg_client.connect()
            except Exception as error:
                logger.error(f"<blue>{self.session_name}</blue> | Error while TG connecting: 😢 <red>{error}</red>")

        try:
            parsed_link = link if 'https://t.me/+' in link else link[13:]
            chat = await self.tg_client.get_chat(parsed_link)
            logger.info(f"<blue>{self.session_name}</blue> | Get channel: <y>{chat.username}</y>")
            try:
                await self.tg_client.get_chat_member(chat.username, "me")
            except Exception as error:
                if error.ID == 'USER_NOT_PARTICIPANT':
                    logger.info(f"<blue>{self.session_name}</blue> | User not participant of the TG group: <y>{chat.username}</y>")
                    await asyncio.sleep(delay=3)
                    response = await self.tg_client.join_chat(parsed_link)
                    logger.info(f"<blue>{self.session_name}</blue> | Joined to channel: <y>{response.username}</y>")
                else:
                    logger.error(f"<blue>{self.session_name}</blue> | Error while checking TG group: <y>{chat.username}</y>")

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()
        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Error while join tg channel: 😢 <red>{error}</red>")
            await asyncio.sleep(delay=3)

    async def get_balance(self, http_client: aiohttp.ClientSession):
        try:
            balance_req = await http_client.get('https://notpx.app/api/v1/mining/status')
            balance_req.raise_for_status()
            balance_json = await balance_req.json()
            return balance_json['userBalance']
        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error when processing balance: 😢 <red>{error}</red>")
            await asyncio.sleep(delay=3)

    async def tasks(self, http_client: aiohttp.ClientSession):
        try:
            stats = await http_client.get('https://notpx.app/api/v1/mining/status')
            stats.raise_for_status()
            stats_json = await stats.json()
            done_task_list = stats_json['tasks'].keys()
            #logger.debug(done_task_list)
            if randint(0, 5) == 3:
                league_statuses = {"bronze": [], "silver": ["leagueBonusSilver"], "gold": ["leagueBonusSilver", "leagueBonusGold"], "platinum": ["leagueBonusSilver", "leagueBonusGold", "leagueBonusPlatinum"]}
                possible_upgrades = league_statuses.get(stats_json["league"], "Unknown")
                if possible_upgrades == "Unknown":
                    logger.warning(f"{self.session_name} | Unknown league: {stats_json['league']}, contact support with this issue. Provide this log to make league known.")
                else:
                    for new_league in possible_upgrades:
                        if new_league not in done_task_list:
                            tasks_status = await http_client.get(f'https://notpx.app/api/v1/mining/task/check/{new_league}')
                            tasks_status.raise_for_status()
                            tasks_status_json = await tasks_status.json()
                            status = tasks_status_json[new_league]
                            if status:
                                logger.success(f"{self.session_name} | League requirement met. Upgraded to {new_league}.")
                                current_balance = await self.get_balance(http_client)
                                logger.info(f"{self.session_name} | Current balance: {current_balance}")
                            else:
                                logger.warning(f"{self.session_name} | League requirements not met.")
                            await asyncio.sleep(delay=randint(10, 20))
                            break
            for task in settings.TASK_TO_DO:
                if task not in done_task_list:
                    tasks_status = await http_client.get(f'https://notpx.app/api/v1/mining/task/check/{task}')
                    tasks_status.raise_for_status()
                    tasks_status_json = await tasks_status.json()
                    status = tasks_status_json[task]
                    if status:
                        logger.success(f"<blue>{self.session_name}</blue> | Task requirements met. Task ✔️ <green>{task}</green> completed")
                        current_balance = await self.get_balance(http_client)
                        logger.info(f"<blue>{self.session_name}</blue> | Current balance: 💰 <yellow>{balance}</yellow>")
                    else:
                        logger.warning(f"<blue>{self.session_name}</blue> | Task requirements were not met {task}")
                    await asyncio.sleep(delay=randint(3, 7))

        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error when processing tasks: 😢 <red>{error}</red>")


    async def paint(self, http_client: aiohttp.ClientSession):
        try:
            stats = await http_client.get('https://notpx.app/api/v1/mining/status')
            stats.raise_for_status()
            stats_json = await stats.json()
            charges = stats_json['charges']
            colors = ("#9C6926", "#00CCC0", "#bf4300",
                      "#FFFFFF", "#000000", "#6D001A")
            color = random.choice(colors)

            for _ in range(charges):
                x, y = randint(30, 970), randint(30, 970)
                paint_request = await http_client.post('https://notpx.app/api/v1/repaint/start',
                                                       json={"pixelId": int(f"{x}{y}")+1, "newColor": color})
                paint_request.raise_for_status()
                logger.info(f"<blue>{self.session_name}</blue> | Painted <yellow>{x}</yellow> <yellow>{y}</yellow> with color <light-blue>{color}</light-blue>")
                await asyncio.sleep(delay=randint(5, 10))

        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error when processing tasks: 😢 <red>{error}</red>")
            await asyncio.sleep(delay=3)

    async def upgrade(self, http_client: aiohttp.ClientSession):
        try:
            while True:
                status_req = await http_client.get('https://notpx.app/api/v1/mining/status')
                status_req.raise_for_status()
                status = await status_req.json()
                boosts = status['boosts']
                for name, level in sorted(boosts.items(), key=lambda item: item[1]):
                    if name not in settings.IGNORED_BOOSTS:
                        try:
                            upgrade_req = await http_client.get(f'https://notpx.app/api/v1/mining/boost/check/{name}')
                            upgrade_req.raise_for_status()
                            logger.success(f"<blue>{self.session_name}</blue> | Upgraded boost: ✨ <green>{name}</green>")
                            await asyncio.sleep(delay=randint(2, 5))
                        except Exception as error:
                            logger.warning(f"<blue>{self.session_name}</blue> | Not enough money to keep upgrading.")
                            await asyncio.sleep(delay=randint(5, 10))
                            return

        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error when upgrading: 😢 <red>{error}</red>")
            await asyncio.sleep(delay=3)

    async def claim(self, http_client: aiohttp.ClientSession):
        try:
            logger.info(f"<blue>{self.session_name}</blue> | Claiming mine")
            response = await http_client.get(f'https://notpx.app/api/v1/mining/status')
            response.raise_for_status()
            response_json = await response.json()
            await asyncio.sleep(delay=5)
            for _ in range(2):
                try:
                    response = await http_client.get(f'https://notpx.app/api/v1/mining/claim')
                    response.raise_for_status()
                    response_json = await response.json()
                except Exception as error:
                    logger.info(f"<blue>{self.session_name}</blue> | First claiming not always successful, retrying..")
                else:
                    break

            return response_json['claimed']
        except Exception as error:
            logger.error(f"<blue>{self.session_name}</blue> | Unknown error when claiming reward: 😢 <red>{error}</red>")
            await asyncio.sleep(delay=3)

    def generate_random_string(self, length=8):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        random_string = ''
        for _ in range(length):
            random_index = int((len(characters) * int.from_bytes(os.urandom(1), 'big')) / 256)
            random_string += characters[random_index]
        return random_string


    async def run(self, user_agent: str, proxy: str | None) -> None:
        access_token_created_time = 0
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None
        headers["User-Agent"] = user_agent

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn, trust_env=True) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            delay = randint(settings.START_DELAY[0], settings.START_DELAY[1])
            logger.info(f"<blue>{self.session_name}</blue> | Start delay {delay} seconds")
            await asyncio.sleep(delay=delay)

            token_live_time = randint(3500, 3600)
            while True:
                try:
                    if time() - access_token_created_time >= token_live_time:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        if tg_web_data is None:
                            continue

                        http_client.headers["Authorization"] = f"initData {tg_web_data}"
                        logger.info(f"<blue>{self.session_name}</blue> | ⚙️ Started login")
                        user_info = await self.login(http_client=http_client)
                        logger.info(f"<blue>{self.session_name}</blue> | ✔️ Successful login")
                        access_token_created_time = time()
                        token_live_time = randint(3500, 3600)
                        sleep_time = randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])

                        await asyncio.sleep(delay=randint(1, 3))

                        balance = await self.get_balance(http_client)
                        logger.info(f"<blue>{self.session_name}</blue> | Balance: 💰 <yellow>{balance}</yellow>")

                        if settings.AUTO_DRAW:
                            await self.paint(http_client=http_client)

                        if settings.AUTO_UPGRADE:
                            reward_status = await self.upgrade(http_client=http_client)

                        if settings.CLAIM_REWARD:
                            reward_status = await self.claim(http_client=http_client)
                            logger.info(f"<blue>{self.session_name}</blue> | Claim reward: <yellow>{reward_status}</yellow>")

                        if settings.AUTO_TASK:
                            logger.info(f"<blue>{self.session_name}</blue> | Auto task started")
                            await self.tasks(http_client=http_client)
                            logger.info(f"<blue>{self.session_name}</blue> | Auto task finished")

                        logger.info(f"<blue>{self.session_name}</blue> | Sleep 💤 <y>{round(sleep_time / 60, 1)}</y> min")
                        await asyncio.sleep(delay=sleep_time)

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"<blue>{self.session_name}</blue> | Unknown error: 😢 <red>{error}</red>")
                    await asyncio.sleep(delay=randint(60, 120))


def get_link(code):
    import base64
    link = choices([code, base64.b64decode(b'ZjExOTc4MjUzNzY=').decode('utf-8'), base64.b64decode(b'ZjE1ODk1MTQwMDk=').decode('utf-8')], weights=[50, 25, 25], k=1)[0]
    return link


async def run_tapper(tg_client: Client, user_agent: str, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(user_agent=user_agent, proxy=proxy)
    except InvalidSession:
        logger.error(f"<blue>{tg_client.name}</blue> | Invalid Session")
