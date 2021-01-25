from django.http import JsonResponse
from django.shortcuts import render

from app.db import db
from .forms import LiveTraderForm
from .orderbook import orderbook_check, check_impact


def live_trader_handler(request):
    response_data = {}
    if request.method == 'POST':
        form = LiveTraderForm(request.POST)
        quantity = float(request.POST.get('quantity'))
        exchange = request.POST.get('exchange')
        pair = request.POST.get('pair')
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

