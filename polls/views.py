# -*- mode: python ; coding: utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from ankr import AnkrWeb3
import demjson
import json
from django.conf import settings
from ankr.types import Blockchain
import requests
from collections import OrderedDict
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

ankr_w3 = AnkrWeb3()

current_eth_price = 0.00 # eth实时价格

async def get_token_prices():
    eth_price = ankr_w3.token.get_token_price(
        blockchain=Blockchain.BSC, 
        contract_address='0x2170ed0880ac9a755fd29b2688956bd959f933f8'
    )
    return eth_price


async def index(request):
    global current_eth_price
    current_eth_price = await get_token_prices()
    current_eth_price  = float(current_eth_price)
    return render(request, "index.html")


def one_wallet(request):
    address = request.GET.get("w_address")
    views = show_one(address)
    return HttpResponse(views)


def show_one(address):
    views = []
    json_result = {}
    assets = ankr_w3.token.get_account_balance(
        wallet_address=address,
        blockchain=settings.BLOCKCHAIN,
    )
    
    for v in assets:
        node_value = str(v).replace(' ', ',')
        node_value = node_value.replace('=', ':')
        node_value = node_value.replace('None', '\'None\'')
        node_value = '{' + node_value + '}'
        node_value = demjson.decode(node_value)
        node_value['balance_usd'] = str(round(float(node_value['balance_usd']),2))
        views.append(node_value)

    holder_address = views[0]['holder_address']
    total_usd = 0.00

    for v in views:
        total_usd += float(v['balance_usd'])
        
    
    json_result.update({'holder_address': holder_address})
    json_result.update({'rec': views})
    json_result.update({'total_usd': str(round(total_usd,2))})
    json_result.update({'total_eth': str(round(total_usd/current_eth_price, 5))})
    json_result['rec'].sort(key = lambda x:x["balance_usd"], reverse=True)
    rec = json_result['rec']

    for v in rec:
        x = float(v['balance_usd'])
        z = x/total_usd
        z = str(round(float(z * 100), 2))
        v.update({'percent': z})
    
    json_result.update({'current_eth': current_eth_price})
    json_result = json.dumps(json_result)
    
    return json_result
    # return render(request, "index.html", {"view_list": views})



