from stellar_sdk import Keypair, Server, TransactionBuilder, Network, Asset, helpers
from operator import itemgetter
from stellar_sdk import AiohttpClient, Server
import asyncio

HORIZON_URL = "https://horizon.stellar.org"


async def transactions():
    async with Server(HORIZON_URL, AiohttpClient()) as server:
        async for transaction in server.transactions().cursor(cursor="now").stream():
            print(f"Transaction: {transaction}")


async def listen():
    await asyncio.gather(transactions())


asyncio.run(listen())