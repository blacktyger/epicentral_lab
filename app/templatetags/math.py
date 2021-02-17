import datetime
import time
from decimal import InvalidOperation, Decimal

import pytz
from django import template
from django.utils.timezone import make_aware
from pytz import NonExistentTimeError, AmbiguousTimeError

from app.db import db

register = template.Library()


def t_s(timestamp):
    """ Convert different timestamps to datetime object"""
    try:
        if len(str(timestamp)) == 13:
            time = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        elif len(str(timestamp)) == 10:
            time = datetime.datetime.fromtimestamp(int(timestamp))
        elif len(str(timestamp)) == 16:
            time = datetime.datetime.fromtimestamp(int(timestamp / 1000000))
        elif len(str(timestamp)) == 12:
            time = datetime.datetime.fromtimestamp(int(timestamp.split('.')[0]))

        else:
            # print(f"{warn_msg} Problems with timestamp: {timestamp}, len: {len(str(timestamp))}")
            pass
        try:
            return make_aware(time)

        except (NonExistentTimeError, AmbiguousTimeError):
            timezone = pytz.timezone('Europe/London')
            time = timezone.localize(time, is_dst=False)
            return time

    except UnboundLocalError as er:
        return timestamp


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



