# -*- mode: python ; coding: utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse 
from django.shortcuts import render
from ankr import AnkrWeb3
import demjson
from django.conf import settings

ankr_w3 = AnkrWeb3()

def index(request):
    return render(request, "index.html")

def one_wallet(request):
    address = request.GET.get("w_address")
    print('address input:', address)
    views = show_one(address)
    return HttpResponse(views) 

def show_one(address):
    views = []
    assets = ankr_w3.token.get_account_balance(
            wallet_address=address,
            blockchain=["eth", "arbitrum", "Optimism"],
        )
    node_list = []
    for v in assets:
        node_value = str(v).replace(' ', ', ')
        node_value = node_value.replace('=', ': ')
        node_value = node_value.replace('None', '\'None\'')
        node_value = '{' + node_value+ '}'
        node_value = demjson.decode(node_value)
        node_list.append(node_value)
    views.append(node_list)
    return views
    # return render(request, "index.html", {"view_list": views})

def show_list(request, wallet_list):
    views = []
    i = 0
    while i < len(wallet_list):
        # print ("address"+str(i)+":", wallet_list[i])    
        assets = ankr_w3.token.get_account_balance(
            wallet_address=wallet_list[i],
            blockchain=settings.BLOCKCHAIN,
        )

        node_list = []
        for v in assets:
            node_value = str(v).replace(' ', ', ')
            node_value = node_value.replace('=', ': ')
            node_value = node_value.replace('None', '\'None\'')
            node_value = '{' + node_value+ '}'
            node_value = demjson.decode(node_value)
            node_list.append(node_value)
        views.append(node_list)
        i += 1
    print(len(views))
    # print(views)
    # return HttpResponse(list(views))
    return render(request, "index.html", {"view_list": views})