import os
import requests
from web3 import Web3
from uniswap import Uniswap
from uniswap.uniswap import AddressLike, _str_to_addr
import etherscan

from price.manager.abis import epic_abi


os.environ["PROVIDER"] = "https://mainnet.infura.io/v3/df2b18f315794e6b9d27bbcaf07310eb"
w3 = Web3(Web3.HTTPProvider(os.environ["PROVIDER"]))

"https://api.uniswap.info/v2/trades/0x4149195911eb592307d9acb08ac6a5de08b8717d_0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

# TOKEN ADDRESSES
# eth_epic = _str_to_addr("0xc27908ed2f80dd8a799625114730f9f10cf89d94")
# eth_fepic = _str_to_addr("0xbffddac07b60e9b564b93cf1f92b4734275f5377")
# epic = _str_to_addr("0x4149195911eb592307d9acb08ac6a5de08b8717d")
# fepic = _str_to_addr("0xeefb1d06d28286216e5d7068f9ef21e01f4dd793")
# weth = _str_to_addr("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
# eth = _str_to_addr("0x0000000000000000000000000000000000000000")
# bat = _str_to_addr("0x0D8775F648430679A709E98d2b0Cb6250d2887EF")
# dai = _str_to_addr("0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359")
#
# my_add = _str_to_addr("0xFA712A2778EF4C1C87FA5fcfef613dB621473f62")
#
# # QUERY INSTANCES
# w3_epic = w3.eth.contract(epic, abi=epic_abi)
# w3_fepic = w3.eth.contract(fepic, abi=epic_abi)
# w3_weth = w3.eth.contract(weth, abi=epic_abi)
# w3_epic_eth = w3.eth.contract(eth_epic, abi=epic_abi)
# w3_fepic_eth = w3.eth.contract(eth_fepic, abi=epic_abi)
# my_acc = Uniswap(address=my_add, private_key="", version=2)
# uni_epic_eth = Uniswap(address=eth_epic, private_key="", version=2)
# uni_fepic_eth = Uniswap(address=eth_fepic, private_key="", version=2)
# uni_epic = Uniswap(address=epic, private_key="", version=2)
# uni_weth = Uniswap(address=weth, private_key="", version=2)
#
# def eth_price():
#     return requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").json()['USD']


# print(w3_epic.functions.getEthToTokenInputPrice().call())
# print('DAI: ')
# print('get_fee_maker: ', uni_epic_eth.get_fee_maker())
# print('get_fee_taker: ', uni_epic_eth.get_fee_taker())
# print('get_eth_token_input_price: ', uni_epic_eth.get_eth_token_input_price(epic, 1 * 10**18) / 10**18)
# print('get_token_eth_input_price: ', uni_epic_eth.get_token_eth_input_price(epic, 1 * 10**18) / 10**18)
# print('get_eth_token_output_price: ', uni_epic_eth.get_eth_token_output_price(epic, 1 * 10**18) / 10**18)
# print('get_token_eth_output_price: ', uni_epic_eth.get_token_eth_output_price(epic, 1 * 10**18) / 10**18)
# print('get_token_balance: ', uni_epic_eth.get_token_balance(epic) / 10**18)
# print('get_token_balance: ', uni_epic_eth.get_token_balance(weth) / 10**18)
# print('liquidity: ', (uni_epic_eth.get_token_balance(weth) / 10**18) * 2 * eth_price())

# print('get_eth_balance: ', uni_epic_eth.get_eth_balance() / 10**18)


# PRINTS
# num = 36
# titles = [" WETH - EPIC ", " WETH - FEPIC "]
#
#
# def print_title(title):
#     d = (num - len(title)) // 2
#     return print(f"{'-' * d}{title} {'-' * d}")
#
#
# # Getting price average price of token with given quantity
# r = [10, 500, 1000, 5000]
#
#
# def show_balance(pair, token, abi=epic_abi):
#     contract = w3.eth.contract(token, abi=abi)
#     name = contract.functions.name().call()
#     symbol = contract.functions.symbol().call()
#     decimals = contract.functions.decimals().call()
#     balance = round(pair.get_token_balance(token) / 10 ** decimals, 2)
#     return print(f"BALANCE: {balance} {symbol}".center(num))
#
#
# def pair_price(pair, tokens):
#     tokens_details = {}
#     temp = []
#     prices = []
#     for token in tokens:
#         decimals = token.functions.decimals().call()
#         symbol = token.functions.symbol().call()
#         balance = round(token.functions.balanceOf(pair.address).call() / 10 ** decimals, 2)
#         # print(f"{symbol}: DEC: {decimals}, BALANCE: {balance}")
#         tokens_details[symbol] = {'symbol': symbol, 'decimals': decimals,
#                                   'balance': balance}
#         temp.append(balance)
#
#     prices.append(temp[1] / temp[0])
#     prices.append(temp[0] / temp[1])
#
#     for i, token in enumerate(tokens):
#         symbol = token.functions.symbol().call()
#         tokens_details[symbol]['price'] = round(prices[i], 4)
#
#     # print(tokens_details)
#     return tokens_details
#
#
# uniswap_wrapper = Uniswap("0x0000000000000000000000000000000000000000",
#                           private_key=None, version=2)
#
# YOUR_API_KEY = str("75YQTX617KH2JAEDEDU722IGMA9QH3ZCAV")
#
# es = etherscan.Client(api_key=YOUR_API_KEY)
#
# # print(f"")
# #
# epic_eth_data = pair_price(w3_epic_eth, [w3_epic, w3_weth])
# epic_dolar_price = round(epic_eth_data['EPIC']['price'] * eth_price(), 2)
# print_title(titles[0])
# print(f"LIQUIDITY: ${round(epic_eth_data['EPIC']['balance'] * epic_dolar_price, 0) * 2}".center(num))
# print(f"PRICE: 1 EPIC for {str(epic_eth_data['EPIC']['price'])} WETH (${epic_dolar_price})".center(num))
# show_balance(uni_epic_eth, epic)
# show_balance(uni_epic_eth, weth)
#
#
# for i in r:
#     print(f"{'-' * num}")
#     price = uni_epic_eth.get_token_eth_input_price(epic, i * 10**18) / 10**18
#     price2 = uni_epic_eth.get_eth_token_output_price(epic, i * 10**18) / 10**18
#     print(f"{i} EPICS FOR {(round(price2, 5))} ETH  [${(round(price2 * eth_price(), 2)) }]")
#     print(f" ** PRICE FOR 1 EPIC [ETH: {(round(price2 / i, 8))}] [${(round((price2 / i) * eth_price(), 2)) }]")
#
#     print(f"{i} EPICS FOR ${(round(price2 * eth_price(), 2)) }")
#     print(f" ** PRICE FOR 1 EPIC ${(round((price2 / i) * eth_price(), 2)) }")
#     print(f"")
#
# fepic_eth_data = pair_price(w3_fepic_eth, [w3_fepic, w3_weth])
# fepic_dolar_price = round(fepic_eth_data['FEPIC']['price'] * eth_price(), 2)
# print_title(titles[1])
# print(f"LIQUIDITY: ${round(fepic_eth_data['FEPIC']['balance'] * fepic_dolar_price, 0) * 2}".center(num))
# print(f"PRICE: 1 FEPIC for {str(fepic_eth_data['FEPIC']['price'])} WETH (${fepic_dolar_price})".center(num))
# show_balance(uni_fepic_eth, fepic)
# show_balance(uni_fepic_eth, weth)
#
# print(f"{'-' * num}")


# print(f"My Balance FEPIC: {my_acc.get_token_balance(fepic) / 10**8}")
# print(f"weth: {uni_weth.get_eth_token_input_price(eth_epic, 10**18)}")

# fepic_eth_data = pair_price(w3_fepic_eth, [w3_fepic, w3_weth])
# print(fepic_eth_data)

def eth_price():
    return requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").json()['USD']


eth_epic = _str_to_addr("0xc27908ed2f80dd8a799625114730f9f10cf89d94")
eth_fepic = _str_to_addr("0xbffddac07b60e9b564b93cf1f92b4734275f5377")
epic = _str_to_addr("0x4149195911eb592307d9acb08ac6a5de08b8717d")
fepic = _str_to_addr("0xeefb1d06d28286216e5d7068f9ef21e01f4dd793")
weth = _str_to_addr("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
eth = _str_to_addr("0x0000000000000000000000000000000000000000")

uni_epic_eth = Uniswap(address=eth_epic, private_key="", version=2)
uni_fepic_eth = Uniswap(address=eth_fepic, private_key="", version=2)
uni_epic = Uniswap(address=epic, private_key="", version=2)
uni_weth = Uniswap(address=weth, private_key="", version=2)

print('EPIC-WETH')
print('get_token_balance weth: ', uni_epic_eth.get_token_balance(weth) / 10**18)
print('get_token_balance epic: ', uni_epic_eth.get_token_balance(epic) / 10**18)
print('liquidity: ', (uni_epic_eth.get_token_balance(weth) / 10**18) * 2 * eth_price())

print('FEPIC-WETH')
print('get_token_balance weth: ', uni_fepic_eth.get_token_balance(weth) / 10**18)
print('get_token_balance fepic: ', uni_fepic_eth.get_token_balance(fepic) / 10**8)
print('liquidity: ', (uni_fepic_eth.get_token_balance(weth) / 10**18) * 2 * eth_price())
