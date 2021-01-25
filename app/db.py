import json
from decimal import InvalidOperation, Decimal

from live_trader import citex_api as citex
import requests
from vitex_api_pkg import VitexRestApi


def d(value, places=8):
    try:
        return round(Decimal(value), places)
    except (InvalidOperation, ValueError):
        if value == '' or ' ' or []:
            print(f'Empty string')
            return Decimal(0)
        else:
            print(f'String should have numbers only')
            pass


class DataBase:
    def __init__(self):
        print("--------------------- INITIALIZE DB ----------------")
        self.btc_price = float(json.loads(requests.get("https://blockchain.info/ticker").content)['USD']['last'])
        self.currency = self.currency_data()
        self.epic = self.epic_data()
        self.blocks = self.block_data()
        self.epic_vs_usd = float(self.epic['usdt']['avg_price'])
        self.epic_vs_btc = float(self.epic['btc']['avg_price'])
        self.orderbook = self.get_orderbook()

    def epicradar_api(self, query):
        base = "https://epicradar.tech/api/"
        url = f"{base}{query}"
        return json.loads(requests.get(url).content)

    def currency_data(self):
        data = self.epicradar_api('currency')
        output = {}
        for x in data:
            output[x['symbol']] = {'flag': x['flag'], 'country': x['country'],
                                   'symbol': x['symbol'], 'price': x['price']}
        return output

    def epic_data(self):
        data = self.epicradar_api('data')
        output = {}
        for x in data:
            output[x['pair']] = x
        return output

    def block_data(self):
        data = self.epicradar_api('block')
        return data

    def get_orderbook(self):
        vitex_api = VitexRestApi()
        vitex_epic_btc_orderbook = vitex_api.get_order_book_depth(symbol="EPIC-001_BTC-000")
        citex_epic_btc_orderbook = citex.get_order_book('EPIC-BTC')
        citex_epic_usdt_orderbook = citex.get_order_book('EPIC-USDT')

        # self.orderbook = {
        #     'vitex': {
        #         'btc': {
        #             'bids': vitex_epic_btc_orderbook['data']['asks'],
        #             'asks': vitex_epic_btc_orderbook['data']['bids']
        #             }},
        #     'citex': {
        #         'btc': {
        #             'bids': vitex_epic_btc_orderbook['data']['asks'],
        #             'asks': vitex_epic_btc_orderbook['data']['asks'],
        #             },
        #         'usd': {
        #             'bids': vitex_epic_btc_orderbook['data']['asks'],
        #             'asks': vitex_epic_btc_orderbook['data']['asks'],
        #             }}
        #     }


        self.orderbook = {
            'vitex': {
                'btc': {
                    'bids': vitex_epic_btc_orderbook['data']['asks'],
                    'asks': vitex_epic_btc_orderbook['data']['bids']
                    }},
            'citex': {
                'btc': {
                    'bids': [[x['price'], x['quantity']] for x in citex_epic_btc_orderbook['data']['asks']],
                    'asks': [[x['price'], x['quantity']] for x in citex_epic_btc_orderbook['data']['bids']],
                    },
                'usd': {
                    'bids': [[x['price'], x['quantity']] for x in citex_epic_usdt_orderbook['data']['asks']],
                    'asks': [[x['price'], x['quantity']] for x in citex_epic_usdt_orderbook['data']['bids']],
                    }}
            }
        return self.orderbook


db = DataBase()
