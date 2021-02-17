# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.views import HomeView, pages, CurrencyToEpicJsonView, price_chart, XLM_EPICJsonView
from app.dash_apps.finished_apps import simpleexample

urlpatterns = [
    re_path(r'^.*\.html', pages, name='pages'),
    path('', HomeView.as_view(), name='home'),
    path('currency_json/', CurrencyToEpicJsonView.as_view(), name='home_currency'),
    path('xlm_sepic_json/', XLM_EPICJsonView.as_view(), name='home_xlm_sepic'),
    path('price_chart/', price_chart, name='price_chart'),
    ]

