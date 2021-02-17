from django import forms
from django.forms import TextInput, NumberInput, RadioSelect, Select


SIDES = [('buy', 'Buy'), ('sell', 'Sell')]
PAIRS = [('btc', 'Bitcoin'), ('usd', 'USD(T)')]
EXCHANGES = [('vitex', 'ViteX'), ('citex', 'Citex')]


class LiveTraderForm(forms.Form):
    amount = forms.FloatField(widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "amount_input",
        'placeholder': '0.00',
        'autocomplete ': 'off'
        }))
    side = forms.ChoiceField(choices=SIDES, widget=Select(attrs={
        'class': "form-control text-white",
        'id': "side_input",
        # 'placeholder': '0.00'
        }))
    pair = forms.ChoiceField(choices=PAIRS, widget=Select(attrs={
        'class': "form-control text-white",
        'id': "pair_input",
        # 'placeholder': '0.00'
        }))
    exchange = forms.ChoiceField(choices=EXCHANGES, widget=Select(attrs={
        'class': "form-control text-white",
        'id': "exchange_input",
        # 'placeholder': '0.00'
        }))


class StellarTraderForm(forms.Form):
    spend = forms.FloatField(widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "spend",
        'placeholder': '0.00',
        'autocomplete ': 'off',
        'style': "font-size: 1.2rem;"
        }), required=False)

    buy = forms.FloatField(widget=NumberInput(attrs={
        'class': "form-control text-white",
        'id': "buy",
        'placeholder': '0.00',
        'autocomplete ': 'off',
        'style': "font-size: 1.2rem;"
        }), required=False)
