# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.views import HomeView, pages, CurrencyToEpicJsonView

urlpatterns = [
    re_path(r'^.*\.html', pages, name='pages'),
    path('', HomeView.as_view(), name='home'),
    path('currency_json/', CurrencyToEpicJsonView.as_view(), name='home_currency'),

    ]

