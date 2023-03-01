# -*- mode: python ; coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from pathlib import Path
from django.conf import settings
import xlrd
from ankr import AnkrWeb3
import demjson
import json
import requests
from django.http import JsonResponse
from ankr.types import Blockchain
ankr_w3 = AnkrWeb3()

current_eth_price = 0.00 # eth实时价格

@csrf_exempt

def handle_upload(request):
    address_list = []
    File = request.FILES.get("file")
    filePath = os.path.join(settings.UPLOAD_ROOT, File.name)
    wb = xlrd.open_workbook(filename=None, file_contents=File.read())
    sheet0 = wb.sheets()[0]
    nrows = sheet0.nrows

    for x in range(0, nrows):
        rowValues = sheet0.row_values(x)
        address_list.append(rowValues[0])

    views = show_list(address_list)
    views = json.dumps(views)
    # print(views)
    
    return HttpResponse(views) 

def get_token_prices():
    eth_price = ankr_w3.token.get_token_price(
        blockchain=Blockchain.BSC, 
        contract_address='0x2170ed0880ac9a755fd29b2688956bd959f933f8'
    )
    return float(eth_price)

def show_list(wallet_list):
    global current_eth_price
    current_eth_price = get_token_prices()

    json_list = []

    i = 0
    while i < len(wallet_list):
        assets = ankr_w3.token.get_account_balance(
            wallet_address=wallet_list[i],
            blockchain=settings.BLOCKCHAIN,
        )
        views = []
        json_result = {}
        for v in assets:
            node_value = str(v).replace(' ', ', ')
            node_value = node_value.replace('=', ': ')
            node_value = node_value.replace('None', '\'None\'')
            node_value = '{' + node_value + '}'
            node_value = demjson.decode(node_value)
            node_value['balance_usd'] = str(round(float(node_value['balance_usd']),2))
            views.append(node_value)
        total_usd = 0.00
        for v in views:
            total_usd += float(v['balance_usd'])
        
        json_result.update({'holder_address': wallet_list[i]})
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
        # print('json_result:', json_result)
        json_list.append(json_result)
        i += 1
    return json_list
