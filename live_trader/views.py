import json

from django.http import JsonResponse
from django.shortcuts import render
import uuid
from simhash import Simhash
from app.db import db
from app.manager.apimanager import APIManager
from app.manager.stellar import LiveTrade
from .forms import LiveTraderForm, StellarTraderForm
from .orderbook import orderbook_check, check_impact

"""
>> Check if user send XLM
    > find transaction with given amount of xlm,

>> Construct payment
    > build transaction  
    > 
"""

stellar = APIManager().stellar
manager = LiveTrade(stellar, destination_asset=stellar.assets['sepic'])


def stellar_transaction_form(request):
    if request.method == 'GET' and request.GET.get('status') == 'user_confirmed':
        response_data = {'status': 'processing data'}
        temp_tx = manager.tx_received[0]
        print(f"FOUND TX {temp_tx['memo']}")

        while not manager.listen_for_transaction():
            print(f"PROCESSING {temp_tx}")

        if manager.tx_confirmed:
            tx = manager.tx_confirmed[0]
            tx_payment = manager.extract_transaction(tx)['_embedded']['records'][0]
            params = {
                'send_amount': tx_payment['amount'],
                'dest_min': tx_payment['amount'],
                'send_code': 'XLM',
                'set_timeout': 60,
                'text_memo': temp_tx['receive_address'],
                }

            manager.build_transaction(params)
            manager.send_tx(manager.tx_to_send[0])

            response_data = {'status': 'DONE'}

        else:
            print(f"TX MEMO: {temp_tx['memo']} FAILED")
            response_data = {'status': 'FAILED'}

        # SUMMARY OF TRANSACTION (FAILED OR SUCCESS / DETAILS)
        return JsonResponse(response_data, safe=False)

    if request.method == 'POST':
        epic_amount = float(request.POST.get('epic'))
        xlm_amount = float(request.POST.get('xlm'))
        receive_address = request.POST.get('receive_address')
        receive_method = request.POST.get('receive_method')

        if receive_method == "wallet":
            receive_address = receive_address
        if receive_method == "keybase":
            receive_address = f"keybaseid_{receive_address}"

        tx_simhash = Simhash(f"{epic_amount}{xlm_amount}{receive_method}").value

        proforma = {
            'status': 'WAITING',
            'amount': xlm_amount,
            'destination_amount': epic_amount,
            'destination_min': epic_amount,
            'receive_address': receive_address,
            'receive_method': receive_method,
            'send_address': stellar.wallet['keys']['public'],
            'memo': str(tx_simhash)[:3]
            }

        print(proforma)
        response_data = proforma
        manager.tx_received.append(proforma)

        return JsonResponse(response_data)


def stellar_trader_handler(request):
    response_data = {}
    if request.method == 'POST':
        spend = float(request.POST.get('spend') or None)
        buy = float(request.POST.get('buy') or None)
        pair = 'xlm'
        side = 'buy'
        print(buy, spend, pair, side)

        value = orderbook_check(
            quantity=buy, exchange='stellarx',
            pair=pair, side=side)

        response_data['average'] = round(value['average'], 2)
        response_data['total'] = round(value['total'], 2)
        response_data['new_price'] = round(value['new_price'], 2)
        response_data['impact'] = round(check_impact(value['start_price'], value['new_price']), 2)
        response_data['start_price'] = value['start_price']
        response_data['counter'] = 'USD'

        for x in ['average', 'total', 'new_price', 'start_price']:
            response_data[f"{x}_counter"] = round(response_data[x] * float(db.xlm_price), 2)

        response_data['btc_price'] = db.btc_price
        response_data['exchange'] = 'stellarx'.upper()
        response_data['pair'] = pair.upper()
        response_data['side'] = side.upper()

        return JsonResponse(response_data)

    else:
        form = StellarTraderForm()
        return render(request, 'home.html', {'form': form})


def live_trader_handler(request):
    response_data = {}
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity'))
        exchange = request.POST.get('exchange')
        pair = request.POST.get('pair').lower()
        side = request.POST.get('side')
        print(quantity, exchange, pair, side)
        value = orderbook_check(
            quantity=quantity, exchange=exchange,
            pair=pair, side=side)

        if pair == "btc":
            response_data['average'] = round(value['average'], 8)
            response_data['total'] = round(value['total'], 4)
            response_data['new_price'] = round(value['new_price'], 8)
            response_data['impact'] = round(check_impact(value['start_price'], value['new_price']), 2)
            response_data['start_price'] = value['start_price']
            response_data['counter'] = 'USD'

            for x in ['average', 'total', 'new_price', 'start_price']:
                response_data[f"{x}_counter"] = round(response_data[x] * db.btc_price, 2)

        elif pair == "usd":
            response_data['average'] = round(value['average'], 4)
            response_data['total'] = round(value['total'], 2)
            response_data['new_price'] = round(value['new_price'], 4)
            response_data['impact'] = round(check_impact(value['start_price'], value['new_price']), 2)
            response_data['start_price'] = value['start_price']
            response_data['counter'] = 'BTC'

            for x in ['average', 'total', 'new_price', 'start_price']:
                response_data[f"{x}_counter"] = round(response_data[x] / db.btc_price, 8)

        elif pair == "xlm":
            response_data['average'] = round(value['average'], 4)
            response_data['total'] = round(value['total'], 2)
            response_data['new_price'] = round(value['new_price'], 4)
            response_data['impact'] = round(check_impact(value['start_price'], value['new_price']), 2)
            response_data['start_price'] = value['start_price']
            response_data['counter'] = 'USD'

            for x in ['average', 'total', 'new_price', 'start_price']:
                response_data[f"{x}_counter"] = round(response_data[x] / float(db.orderbook.stellar_data()['price']), 8)

        # print(f"{quantity} for {pair} on {exchange}")
        # print(f"------------------------------------")
        # print(f"average price {response_data['average']}")
        # print(f"new price {response_data['new_price']}")
        # print(f"start price {value['start_price']}")
        # print(f"price impact: {round(response_data['impact'], 2)}%")

        response_data['btc_price'] = db.btc_price
        response_data['quantity'] = quantity
        response_data['exchange'] = exchange.upper()
        response_data['pair'] = pair.upper()
        response_data['side'] = side.upper()

        return JsonResponse(response_data)

    else:
        form = LiveTraderForm()
    return render(request, 'home.html', {'form': form})

