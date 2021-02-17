"""
APIManager - query all Epic-Cash related assets in crypto blockchains.com
"""

from .stellar import *


class APIManager:

    def __init__(self):
        self.stellar = StellarAPI()

