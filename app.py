import datetime
import random
import time

from bot.free_nano_faucet_bot import FreeNanoFaucetBot
from env.config import Config

CONFIG_PATH = 'env/config.json'


def get_config(env):
    return Config(CONFIG_PATH, env)


def show_start_log():
    now = datetime.datetime.now()
    hour_now = '{:d}:{:02d}'.format(now.hour, now.minute)
    print(f"Getting Free Nano Coin at {hour_now}...")


def job():
    show_start_log()
    wallets, faucet, proxy = get_config("wallets"), \
                             get_config("faucet"), \
                             get_config("proxy")

    bot = FreeNanoFaucetBot(faucet, wallets, proxy, with_proxy=False)
    bot.exec()
    bot.teardown()


if __name__ == "__main__":
    while 1:
        job()
        custom_time = random.randint(1, 5)
        time.sleep(custom_time + (10 * 60))
