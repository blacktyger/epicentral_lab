# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # add this
from live_trader.views import stellar_trader_handler, stellar_transaction_form


urlpatterns = [
    path('admin/', admin.site.urls),           # Django admin route
    path("", include("authentication.urls")),  # Auth routes - login / register
    path("", include("app.urls")),             # UI Kits Html files
    path('mining/', include("mining_calculator.urls")),
    # path('trader', include("live_trader.urls")),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('trader/', stellar_trader_handler, name='stellar_trader'),
    path('trader/tx/', stellar_transaction_form, name='stellar_transaction'),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),


    path('blog', include("blog.urls")),
    # path('profile/', profile, name='profile'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)