from django import forms
from django.forms import TextInput, NumberInput, RadioSelect, Select

from app.db import db


SIDES = [('buy', 'Buy'), ('sell', 'Sell')]
PAIRS = [('btc', 'Bitcoin'), ('usd', 'USD(T)')]
EXCHANGES = [('vitex', 'ViteX'), ('citex', 'Citex')]
ALGOS = [('progpow', 'ProgPow (GPU)'), ('randomx',  'RandomX (CPU)')]
CURRENCIES = [(v['symbol'], v['symbol']) for k, v in db.currency.items()]


class MiningCalculatorForm(forms.Form):
    rig_hashrate = forms.IntegerField(widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "rig_hashrate",
        'placeholder': '4000 H/s',
        'autocomplete ': 'off'
        }))
    algo = forms.ChoiceField(initial=ALGOS[1], choices=ALGOS, widget=Select(attrs={
        'class': "form-control text-white",
        'id': "algo",
        # 'placeholder': '0.00'
        }))
    currency = forms.ChoiceField(initial="USD", choices=CURRENCIES, widget=Select(attrs={
        'class': "form-control text-white",
        'id': "currency",
        'value': 'USD',
        # 'placeholder': '0.00'
        }))
    power_consumption = forms.FloatField(required=False, widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "power_consumption",
        'placeholder': '300W',
        }))
    electricity_cost = forms.FloatField(required=False, widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "electricity_cost",
        'placeholder': '0.20 kWH',
        }))
    pool_fee = forms.FloatField(required=False, widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "pool_fee",
        'placeholder': '2%',
        }))
