import json
from decimal import InvalidOperation, Decimal
from statistics import mean

from app.manager.apimanager import APIManager
from live_trader import citex_api as citex
import requests
from app.tools.timer import Timer
from vitex_api_pkg import VitexRestApi
from pycoingecko import CoinGeckoAPI


def to_epic(currency, base="EPIC"):
    if base == "EPIC":
        if currency == ('USD' or 'usd' or 'usdt'):
            return db.epic_vs_usd
        elif currency == ('BTC' or 'btc' or 'bitcoin'):
            return db.epic_vs_btc
        elif currency == ('XLM' or 'xlm' or 'lumen'):
            return db.epic_vs_xlm
        else:
            for k, v in db.currency.items():
                if k == currency:
                    curr_vs_usd = float(v['price'])
                    return db.epic_vs_usd * curr_vs_usd
            else:
                return 1


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


db_inits = 0


class DataBase:
    def __init__(self):
        print("------- DATABASE REPORT ----------------")
        self.cg = CoinGeckoAPI()
        self.btc_price = float(json.loads(requests.get("https://blockchain.info/ticker").content)['USD']['last'])
        self.xlm_price = self.cg.get_price(ids=['STELLAR'], vs_currencies=['USD'])['stellar']['usd']
        self.currency = self.currency_data()
        self.epic = self.epic_data()
        self.blocks = self.block_data()
        self.epic_vs_usd = float(self.epic['usdt']['avg_price'])
        self.epic_vs_btc = float(self.epic['btc']['avg_price'])
        self.orderbook = self.get_orderbook()
        self.epic_vs_xlm = self.stellar_data()['sepic_xlm']['price']
        self.add_instance()
        print("-------- END REPORT --------------------\n")

    def add_instance(self):
        global db_inits
        db_inits += 1
        print(f"Database initialize: x {db_inits}")

    def epicradar_api(self, query):
        base = "https://epicradar.tech/api/"
        url = f"{base}{query}"
        return json.loads(requests.get(url).content)

    @Timer(name='epic_chart_price')
    def epic_chart_price(self):
        data = self.cg.get_coin_market_chart_by_id(id='epic', vs_currency="usd", days=1)
        return data

    @Timer(name='currency_data')
    def currency_data(self):
        data = self.epicradar_api('currency')
        data.append({'flag': None, 'country': None,
                     'symbol': 'XLM', 'price': self.xlm_price})
        data.append({'flag': None, 'country': None,
                     'symbol': 'BTC', 'price': self.btc_price})
        output = {}

        for x in data:
            output[x['symbol']] = {'flag': x['flag'], 'country': x['country'],
                                   'symbol': x['symbol'], 'price': x['price']}

        return output

    @Timer(name='epic_data')
    def epic_data(self):
        data = self.epicradar_api('data')
        output = {}
        for x in data:
            output[x['pair']] = x
        return output

    @Timer(name='block_data')
    def block_data(self):
        data = self.epicradar_api('block')
        return data

    @Timer(name='stellar_data')
    def stellar_data(self):
        xlm = APIManager().stellar
        usd = APIManager().stellar
        usd.counter = usd.assets['usd']
        data = {}

        for pair in [xlm, usd]:
            data[f"sepic_{pair.counter.code.lower()}"] = {
                'price': pair.last_trade()['price'],
                'vol_24h': pair.last_24h()['base_volume'],
                'orderbook': pair.orderbook()
                }

        print(data)
        return data

    @Timer(name='get_orderbook')
    def get_orderbook(self):
        vitex_api = VitexRestApi()
        vitex_epic_btc_orderbook = vitex_api.get_order_book_depth(symbol="EPIC-001_BTC-000")
        citex_epic_btc_orderbook = citex.get_order_book('EPIC-BTC')
        citex_epic_usdt_orderbook = citex.get_order_book('EPIC-USDT')
        stellar = self.stellar_data()
        stellarx_sepic_usd_orderbook = stellar['sepic_usd']['orderbook']
        stellarx_sepic_xlm_orderbook = stellar['sepic_xlm']['orderbook']

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
                    }},
            'stellarx': {
                'usd': stellarx_sepic_usd_orderbook,
                'xlm': stellarx_sepic_xlm_orderbook
                },
            }
        return self.orderbook


db = DataBase()


# -------------------
# WHEN CITEX DOWN:
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
