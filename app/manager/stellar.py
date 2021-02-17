import json
import time
import pickle
import requests
import asyncio
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, AiohttpClient
from stellar_sdk import Asset as asset_
import datetime
from operator import itemgetter
from decimal import Decimal


def get_ts(date):
    """ Convert datetime object to timestamp in miliseconds """
    if not isinstance(date, str):
        date = str(date).split(" ")[0]
    else:
        date = date
    return int(time.mktime(time.strptime(date, "%Y-%m-%d"))) * 1000


class LiveTrade:
    def __init__(self, api_manager, destination_asset):
        self.data = api_manager
        self.direct_path = False
        self.best_path = None
        self.destination_asset = destination_asset
        self.source_account = self.init_source_account()
        self.tx_received = []
        self.tx_to_send = []
        self.tx_confirmed = []
        self.tx_history_file = 'local_history_transactions'

    def init_source_account(self):
        self.keys = Keypair.from_secret(self.data.wallet['keys']['private'])
        print(f'INITIALIZE KEYS AND SOURCE ACCOUNT: {self.keys.public_key}')
        return self.data.server.load_account(account_id=self.keys.public_key)

    def get_network_tx(self):
        """
        >> Download blockchain snapshot of transactions for address
        >> compare with local history of transactions, save to lists
        """
        print(f"get_network_tx START")
        full_network_list = []
        transactions = self.data.server.transactions() \
            .for_account(account_id=self.data.wallet['keys']['public']) \
            .order(desc=True).limit(100).call()

        for t in transactions['_embedded']['records']:
            full_network_list.append(t)

        return full_network_list

    def save_network_history(self, data=None):
        if not data:
            data = self.get_network_tx()

        with open(self.tx_history_file, 'wb') as f:
            last_date = data[0]['created_at']
            pickle.dump(data, f)
            print(f"{len(data)} txs saved to file (last: {last_date})")

    def read_local_history(self):
        with open(self.tx_history_file, 'rb') as f:
            data = pickle.load(f)
            last_date = data[0]['created_at']
            print(f"{len(data)} txs read from file (last: {last_date})")
        return data

    def append_to_local_history(self, tx):
        data = self.read_local_history()
        data.insert(0, tx)
        print(data[0])
        self.save_network_history(data=data)

    def extract_transaction(self, tx):
        data = self.data.server.payments(). \
            for_transaction(transaction_hash=tx['hash']).call()
        return data

    def confirmed_in_network(self, network, local):
        """
        > USER TRANSACTION VALIDATION
            >> Compare memo from network tx and received tx (hash from 3 values:
                {epic_amount}{xlm_amount}{receive_method})
            >> If memo is matching return True
            >> If memo don't match compare XLM amount
            >> If XLM amount is different no more than 1% return True
            >> If memo and XLM amount do not match send XLM back to user address
        """
        print(f"confirmed_in_network START")

        def is_amount_valid():
            print(f"is_amount_valid start")
            n = self.extract_transaction(network)['_embedded']['records'][0]
            print(n['amount'], local['amount'])

            if Decimal(local['amount']) == Decimal(n['amount']):
                print(f"source_amount ({local['amount']}) match, but MEMO is different!")
                return True
            else:
                v1 = Decimal(local['amount'])
                v2 = Decimal(n['amount'])
                try:
                    percentage = round(abs(v1 - v2) / max(v1, v2) * 100, 3)
                except ZeroDivisionError:
                    percentage = float('inf')

                print(percentage, '%')
                if percentage < 1.1:
                    return True
                else:
                    self.stats()
                    return False

        if network['memo_type'] != "none":
            print(network['memo_type'])
            print(network['memo'])
            print(local['memo'])

            if network['memo'] == local['memo']:
                print(f"MEMO ({local['memo']} MATCH!")
                return True
            else:
                return is_amount_valid()
        else:
            return is_amount_valid()

    def listen_for_transaction(self):
        """
        >> Get network transaction history for source account
        >> Compare local transaction history with network
        >> while there is no new transaction in network
            >> read_local_history every x sec
            >> if no new tx after x times return True and
                prompt TIME OUT / FAILED
        >> if new transaction's loop over them
            >> check if it was checked before
            >> check if confirmed_in_network
            >> if yes return True
            >> else continue through new_tx list and repeat

         """
        print(f"listen_for_transaction")

        max_try = 10
        local_history = self.read_local_history()
        match = False
        checked_txs = []

        while max_try and not match:
            time.sleep(5)
            max_try = max_try - 1
            print(f"RESFRESHING NETWORK HISTORY || TRY LEFT: {max_try} ...")
            new_tx = [x for x in self.get_network_tx() if x not in local_history]

            if new_tx:
                for i, tx in enumerate(new_tx):
                    if tx not in checked_txs:
                        print(f"NEW TX: {len(new_tx)}")
                        print(f"RECEIVED NEW NETWORK TX({i}) {tx['created_at']}")

                        if self.confirmed_in_network(local=self.tx_received[0], network=tx):
                            self.tx_confirmed.append(tx)
                            match = True
                            return match
                        else:
                            checked_txs.append(tx)

        if not match:
            self.stats()
            print(f"TIME OUT TRANSACTION FAILED")
            return True

    def get_send_paths(self, **kwargs):
        def get_path_asset(record):
            path = record['path'][0]
            asset = asset_(code=path['asset_code'], issuer=path['asset_issuer'])
            print(f'PATH ASSET: {asset.code}')
            return [asset]

        def get_best_path(paths):
            sorted_by_amount = sorted(paths, key=itemgetter('destination_amount'), reverse=True)
            direct = None
            direct_amount = 0
            best_amount = Decimal(sorted_by_amount[0]['destination_amount'])

            for path in sorted_by_amount:
                if not path['path']:
                    direct = path
                    direct_amount = Decimal(path['destination_amount'])

            print(f"{direct_amount} {best_amount}")
            try:
                percentage = abs(direct_amount - best_amount) / max(direct_amount, best_amount) * 100
            except ZeroDivisionError:
                percentage = float('inf')

            print(f"PATHS PERCENTAGE {round(percentage, 3)}%")

            if percentage < 0.5:
                sorted_by_amount.insert(0, direct)
                print(f"PICK DIRECT")

            return sorted_by_amount

        records = self.data.server.strict_send_paths(**kwargs).call()
        paths = []

        for r in records['_embedded']['records']:
            print(r)
            print('\n --------------------------------------------------------')

        for r in records['_embedded']['records']:
            if 'destination_asset_code' in r.keys():
                if r['destination_asset_code'] == self.destination_asset.code:
                    paths.append(r)
                    print('\n2 --------------------------------------------------------')
                    print(r)

        paths = get_best_path(paths)

        if paths[0]['path']:
            paths[0]['path'] = get_path_asset(paths[0])
            print(f"NO DIRECT PATH - BRIDGE ASSET: {paths[0]['path']}")
        return paths[0]

    def build_transaction(self, kwargs):
        if not 'source_asset' in kwargs.keys():
            kwargs['source_asset'] = self.data.assets['xlm']

        base_fee = 100
        source_account = self.source_account
        destination = self.data.epic_gateway_addr
        destination_asset = self.destination_asset
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        send_amount = kwargs['send_amount']
        send_code = kwargs['send_code']
        set_timeout = kwargs['set_timeout']
        text_memo = kwargs['text_memo']

        path = self.get_send_paths(
            source_asset=kwargs['source_asset'],
            source_amount=kwargs['send_amount'],
            destination=self.data.epic_gateway_addr,
            )
        print(path)

        dest_min = path['destination_amount']

        print(f"TRADE {send_amount} {send_code} FOR {dest_min} {destination_asset.code}")

        transaction = TransactionBuilder(
            source_account=source_account,
            network_passphrase=network_passphrase,
            base_fee=base_fee) \
            .append_path_payment_strict_send_op(
            send_code=send_code, send_issuer=None,
            dest_code=destination_asset.code,
            dest_issuer=destination_asset.issuer, send_amount=send_amount,
            dest_min=dest_min, destination=destination,
            path=path['path']) \
            .set_timeout(set_timeout) \
            .add_text_memo(text_memo) \
            .build()
        self.tx_to_send.append(transaction)
        print(f"SEND TRANSACTION ADDED TO QUEUE:")

    def send_tx(self, tx):
        tx.sign(self.keys)
        response = self.data.server.submit_transaction(tx)  # f"TEST SEND SUCCESS"
        print(tx.to_xdr())
        print(f'TX: {tx.hash_hex()} SENDED TO NETWORK')
        print(f'RESPONSE: {response}')
        self.append_to_local_history(self.tx_confirmed[0])
        self.tx_to_send.remove(tx)
        self.tx_received.remove(self.tx_received[0])
        self.tx_confirmed.remove(self.tx_confirmed[0])

        self.stats()
        return response

    def stats(self):
        print(f"""
        ***** STATS *****
        tx_to_send ({len(self.tx_to_send)}): 
        {self.tx_to_send}
        -----------------
        tx_received ({len(self.tx_received)}): 
        {self.tx_received}
        -----------------
        tx_confirmed ({len(self.tx_confirmed)}): 
        {self.tx_confirmed}
        -----------------
        """)


class StellarAPI:
    """
    Class for quick and clean extracting data about trading pairs from Stellar API 'HORIZON'
    default:
    :base: EPIC
    :counter: LUMEN (xlm)
    :server: stellar_sdk Server object
    :assets: EPIC | XLM | USD
    """

    def __init__(self):
        self.server = Server(horizon_url="https://horizon.stellar.org")
        self.assets = {}
        self.init_assets()
        self.base = self.assets['sepic']
        self.counter = self.assets['xlm']
        self.wallet = {
            'keys': {
                'public': "GBYB6Y6SXU2Y7RXGAPWQIXO5IULILZLBLWTRHI6QSWAUGHM3BLF33A3C",
                'private': "SCS4OCUNPOBW3E7MPKYQG7Z3PZC7ZSUF2CITUI3LB3CE7MHABZ2FASXH"
                }
            }
        self.epic_gateway_addr = "GCXAJPJNTN7UQSQW6ZGEUE2Z7JNC2R2CGW4VXGITWFE6OWBPQZ5I2M57"
        self.epic_gateway_addr_2 = "GD6W7XRMXCH6WCET65AMOZK5BABG3M53VKUVIQNIFMW2EVUEV4NCM6K7"

    def init_assets(self):
        self.assets = {
            'xlm': asset_("XLM"),
            'sepic': asset_(code='EPIC', issuer='GD4YEDHMQK2HD7DMKAG554JK4TVOTQNPWTKR2KHL5UCSJ6ART2UA2E32'),
            'usd': asset_(code='USD', issuer='GDUKMGUGDZQK6YHYA5Z6AY2G4XDSZPSZ3SW5UN3ARVMO6QSRDWP5YLEX')
            }

    def add_asset(self, name, code, issuer):
        self.assets[name] = asset_(code=code, issuer=issuer)

    def last_trade(self):
        return self.trades(limit=1)[0]

    def xlm_sepic_send_path(self, amount):
        full_url = f"https://horizon.stellar.org/paths/strict-send?destination_assets=EPIC%3AGD4YEDHMQK2HD7DMKAG554JK4TVOTQNPWTKR2KHL5UCSJ6ART2UA2E32&source_asset_type=native&source_amount={amount}"
        # print(requests.Request('GET', full_url).prepare().url)
        return json.loads(requests.get(full_url).content)

    def xlm_sepic_receive_path(self, amount):
        full_url = f"https://horizon.stellar.org/paths/strict-receive?&destination_asset_type=credit_alphanum4&destination_asset_code=EPIC&destination_asset_issuer=GD4YEDHMQK2HD7DMKAG554JK4TVOTQNPWTKR2KHL5UCSJ6ART2UA2E32&source_assets=native&destination_amount={amount}"
        # print(requests.get(full_url).content)
        return json.loads(requests.get(full_url).content)

    def find_tx(self, amount, address=None):
        pass

    def last_24h(self):
        end_today = datetime.datetime.today() + datetime.timedelta(days=1)
        start_today = datetime.datetime.today()
        try:
            return self.trades(start=get_ts(start_today), end=get_ts(end_today),
                               resolution=86400000)[0]
        except IndexError:
            return self.trades(end=get_ts(end_today), resolution=86400000)[0]

    def orderbook(self):
        """
        Return orderbook dict with :bids and :asks with amount and price
        for given trading pair (:base, :counter) EXAMPLE: EPIC/XLM
        """
        data = self.server.orderbook(self.base, self.counter).call()
        asks = [[float(x['price']),
                 float(x['amount']) / float(x['price'])] for x in data['bids']]

        bids = [[float(x['price']), float(x['amount'])] for x in data['asks']]

        return {'bids': bids, 'asks': asks}

    def trades(self, start=None, end=None, resolution=3600000, limit=10):
        """
        Return dict with last tardes on given pair
        :base :counter - assets
        :start :end - date range (datetime obj or string 'year-month-dat' format)
        :resolution - time interval in miliseconds
        :limit - number of records to show
        """
        data = self.server.trade_aggregations(self.base, self.counter, resolution=resolution,
                                              start_time=start, end_time=end
                                              ).limit(limit).order('dec').call()
        data = [{'time': x['timestamp'], 'trade_count': x['trade_count'],
                 'base_volume': x['base_volume'], 'counter_volume': x['counter_volume'],
                 'price': x['avg'], 'high': x['high'], 'low': x['low'],
                 'open': x['open'], 'close': x['close']} for x in data['_embedded']['records']]
        return data


    # def listen_for_user_tx(self):
    #
    #     HORIZON_URL = "https://horizon.stellar.org"
    #
    #     async def payments():
    #         async with Server(HORIZON_URL, AiohttpClient()) as server:
    #             async for payment in server.payments() \
    #                 .for_account(self.data.wallet['keys']['public']) \
    #                 .cursor(cursor="now").stream():
    #                 print(f"Payment: {payment}")
    #
    #     async def transactions():
    #         async with Server(HORIZON_URL, AiohttpClient()) as server:
    #             async for transaction in server.transactions() \
    #                 .for_account(self.data.wallet['keys']['public']) \
    #                 .cursor(cursor="now").stream():
    #                 print(f"Transaction: {transaction}")
    #
    #     async def listen():
    #         await asyncio.gather(
    #             payments(),
    #             transactions()
    #             )
    #
    #     asyncio.run(listen())
