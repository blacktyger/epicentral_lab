import datetime

import requests
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Select your transport with a defined url endpoint
transport = RequestsHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    {
     pairs(where: {
    id: "0xc27908ed2f80dd8a799625114730f9f10cf89d94"
  }
 ) {
 token1 {
    symbol
    }
  token0 {
    symbol
    }
    totalSupply
    reserveETH
    reserveUSD
    token0Price
    token1Price
    untrackedVolumeUSD
    txCount
 }
    }
    
"""
    )

# Execute the query on the transport
result = client.execute(query)
for k, v in result.items():
    print(k, v)
    for x in v:
        print(x)
        for i, o in x.items():
            print(i, o)

 # pairs(where: {
 #    id: "0xc27908ed2f80dd8a799625114730f9f10cf89d94"
 #  }
 # ) {
 # token1 {
 #    symbol
 #    }
 #  token0 {
 #    symbol
 #    }
 #    totalSupply
 #    reserveETH
 #    reserveUSD
 #    token0Price
 #    token1Price
 #    untrackedVolumeUSD
 #    txCount
 # }

# print(request.content)
# import os
# import requests
# from web3 import Web3
# from uniswap import Uniswap
# from uniswap.uniswap import AddressLike, _str_to_addr
# import etherscan
# from price.manager.abis import epic_abi
#
#
# os.environ["PROVIDER"] = "https://mainnet.infura.io/v3/df2b18f315794e6b9d27bbcaf07310eb"
# w3 = Web3(Web3.HTTPProvider(os.environ["PROVIDER"]))
#
#
# def eth_price():
#     return requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").json()['USD']
#
#
# # TOKEN ADDRESSES
# eth_epic = _str_to_addr("0xc27908ed2f80dd8a799625114730f9f10cf89d94")
# eth_fepic = _str_to_addr("0xbffddac07b60e9b564b93cf1f92b4734275f5377")
# epic = _str_to_addr("0x4149195911eb592307d9acb08ac6a5de08b8717d")
# fepic = _str_to_addr("0xeefb1d06d28286216e5d7068f9ef21e01f4dd793")
# weth = _str_to_addr("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
# eth = _str_to_addr("0x0000000000000000000000000000000000000000")
#
# uni_epic_eth = Uniswap(address=eth_epic, private_key="", version=2)
# uni_fepic_eth = Uniswap(address=eth_fepic, private_key="", version=2)
# uni_epic = Uniswap(address=epic, private_key="", version=2)
# uni_weth = Uniswap(address=weth, private_key="", version=2)
#
# price2 = uni_epic_eth.get_eth_token_output_price(epic, 1 * 10**18) / 10**18
# print(f" 1 EPICS FOR {(round(price2, 5))} ETH  [${(round(price2 * eth_price(), 2)) }]")
# print(f" ** PRICE FOR 1 EPIC ${(round((price2 / 1) * eth_price(), 2)) }")
#
#
# fepic_price2 = uni_fepic_eth.get_eth_token_output_price(fepic, 1 * 10**8) / 10**18
# print(f" 1 EPICS FOR {(round(fepic_price2, 5))} ETH  [${(round(fepic_price2 * eth_price(), 2)) }]")
# print(f" ** PRICE FOR 1 EPIC ${(round((fepic_price2 / 1) * eth_price(), 2)) }")
