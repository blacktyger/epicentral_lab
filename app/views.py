# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.views import generic

from app.templatetags.math import to_epic
from blog.models import Post
from live_trader.forms import LiveTraderForm
from mining_calculator.forms import MiningCalculatorForm
from mining_calculator.mining import Calculator


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
        context['form'] = LiveTraderForm()
        context['calc_form'] = MiningCalculatorForm()
        context['periods'] = [('hour', 1 / 24), ('day', 1), ('week', 7)]

        return context


class CurrencyToEpicJsonView(HomeView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        base = request.GET.get('base')
        currency = request.GET.get('currency')
        value = to_epic(currency=currency)
        return JsonResponse({'value': value})


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
