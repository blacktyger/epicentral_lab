import os
import requests
from web3 import Web3
from uniswap import Uniswap
from uniswap.uniswap import _str_to_addr
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from .uniswapapi import result

os.environ["PROVIDER"] = "https://mainnet.infura.io/v3/df2b18f315794e6b9d27bbcaf07310eb"
transport = RequestsHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")
client = Client(transport=transport, fetch_schema_from_transport=False)


# print('EPIC-WETH')
# print('get_token_balance weth: ', uni_epic_eth.get_token_balance(weth) / 10**18)
# print('get_token_balance epic: ', uni_epic_eth.get_token_balance(epic) / 10**18)
# print('liquidity: ', (uni_epic_eth.get_token_balance(weth) / 10**18) * 2 * eth_price())
#
# print('FEPIC-WETH')
# print('get_token_balance weth: ', uni_fepic_eth.get_token_balance(weth) / 10**18)
# print('get_token_balance fepic: ', uni_fepic_eth.get_token_balance(fepic) / 10**8)
# print('liquidity: ', (uni_fepic_eth.get_token_balance(weth) / 10**18) * 2 * eth_price())


class UniswapAPI:
    """
    Class for quick and clean extracting data from Uniswap GRAPHQL'
    """

    def __init__(self):
        self.init_assets()
        self.eth_price = float(self.ethprice())

    def ethprice(self):
        return requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").json()['USD']

    def init_assets(self):
        self.address = {
            'eth_epic': _str_to_addr("0xc27908ed2f80dd8a799625114730f9f10cf89d94"),
            'eth_fepic': _str_to_addr("0xbffddac07b60e9b564b93cf1f92b4734275f5377"),
            'epic': _str_to_addr("0x4149195911eb592307d9acb08ac6a5de08b8717d"),
            'fepic': _str_to_addr("0xeefb1d06d28286216e5d7068f9ef21e01f4dd793"),
            'weth': _str_to_addr("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
            'eth': _str_to_addr("0x0000000000000000000000000000000000000000"),
            }

        self.pair = {
            'epic_eth': Uniswap(address=self.address['eth_epic'], private_key="", version=2),
            'fepic_eth': Uniswap(address=self.address['eth_fepic'], private_key="", version=2),
            }

    def add_address(self, name, address):
        self.address[name] = _str_to_addr(address)

    def add_pair(self, name, address):
        self.pair[name] = Uniswap(address=address, private_key="", version=2)

    def token_price(self, pair_id, token_id):
        price = pair_id.get_eth_token_output_price(token_id, 1 * 10**18) / 10**18
        print(f" ** PRICE FOR 1 EPIC ${round(price * self.eth_price, 2)}")

    def pool_liquidity(self, pool):
        base = self.address['weth']
        return print('liquidity: ', (pool.get_token_balance(base) / 10**18) * 2 * self.eth_price)

    def epic_liq(self):
        return self.pool_liquidity(pool=self.pair['epic_eth'])

    def epic_price(self):
        return self.token_price(pair_id=self.pair['epic_eth'], token_id=self.address['epic'])

    def test(self, result=result):
        for k, v in result.items():
            print(k, v)
            for x in v:
                print(x)


