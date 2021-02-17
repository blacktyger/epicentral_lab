# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.views import generic

from app.manager.apimanager import APIManager
from app.templatetags.math import t_s
from blog.models import Post
from live_trader.forms import LiveTraderForm, StellarTraderForm
from live_trader.orderbook import orderbook_check
from mining_calculator.forms import MiningCalculatorForm
from mining_calculator.mining import Calculator

from app.db import db, to_epic


class HomeView(generic.ListView):
    template_name = 'home.html'
    app = Calculator(algo='randomx', rig_hashrate=1, currency='USD')
    model = Post

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['mining_c'] = {
            'currency_list': self.app.currency_list,
            'algo_list': self.app.algos,
            }
        context['currency_list'] = self.app.currency_list
        context['algo_list'] = self.app.algos
        # context['form'] = LiveTraderForm()
        context['stellar_form'] = StellarTraderForm()
        context['calc_form'] = MiningCalculatorForm()
        context['periods'] = [('hour', 1 / 24), ('day', 1), ('week', 7)]
        context['send_xlm_address'] = APIManager().stellar.wallet['keys']['public']

        return context


class CurrencyToEpicJsonView(HomeView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        base = request.GET.get('base')
        currency = request.GET.get('currency')
        value = to_epic(currency=currency)
        return JsonResponse({'value': value, 'currency': currency})


class XLM_EPICJsonView(HomeView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        buy = request.GET.get('buy')
        spend = request.GET.get('spend')
        currency = request.GET.get('currency')
        epic_to_xlm = 0
        xlm_to_epic = 0
        stellar = APIManager().stellar

        if spend:
            try:
                xlm_to_epic = stellar.xlm_sepic_send_path(amount=spend)
                xlm_to_epic = xlm_to_epic['_embedded']['records'][0]['destination_amount']
                # print(xlm_to_epic)
            except (TypeError, KeyError) as err:
                print(err)

        if buy:
            try:
                epic_to_xlm = stellar.xlm_sepic_receive_path(amount=buy)
                epic_to_xlm = epic_to_xlm['_embedded']['records'][0]['source_amount']
                # print(epic_to_xlm)
            except (TypeError, KeyError) as err:
                print(err)

        return JsonResponse({'value': {'xlm_to_epic': xlm_to_epic,
                                       'epic_to_xlm': epic_to_xlm},
                             'currency': currency})


def price_chart(request):
    time = []
    price = []

    data = db.db.epic_chart_price()
    for entry in data['prices']:
        time.append(t_s(entry[0]).strftime("%d/%m/%Y %H:%M"))
        price.append(entry[1])
        # print(entry[1])

    return JsonResponse(data={
        'time': time,
        'price': price,
        })


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('home.html')
        return HttpResponse(html_template.render(context, request))
