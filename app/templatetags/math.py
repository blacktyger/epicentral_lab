from decimal import InvalidOperation, Decimal
from django import template
from app.db import db

register = template.Library()


@register.filter(name='to_epic')
def to_epic(currency, base="EPIC"):
    if base == "EPIC":
        if currency == ('USD' or 'usd' or 'usdt'):
            return db.epic_vs_usd
        elif currency == ('BTC' or 'btc' or 'bitcoin'):
            return db.epic_vs_btc
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


@register.filter(name='multi')
def multi(value, num):
    return d(value) * d(num)


@register.filter(name='sub')
def subtract(value, arg):
    return value - arg


@register.filter()
def add(value, num):
    return d(value) + d(num)


@register.filter()
def satoshi(value):
    return d(value) * 100000000


@register.filter()
def get_percent(value, num):
    """
    :param value:
    :param num:
    :return: rounded percentage value of num
    """
    return d(d(value) / d(num) * 100, 2)


@register.filter(name='colour')
def percentage_color(value):
    if value < 20:
        return f"progress-bar-danger"
    elif 20 <= value <= 50:
        return f"progress-bar-warning"
    else:
        return f"progress-bar-success"



