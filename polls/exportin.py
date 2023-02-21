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
ankr_w3 = AnkrWeb3()


@csrf_exempt
def handle_upload(request):
    print("chainlist:", settings.BLOCKCHAIN)
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
    print(type(views))
    print(type(json.dumps(views)))
    return HttpResponse(json.dumps(views)) 

def show_list(wallet_list):
    views = []
    i = 0
    while i < len(wallet_list):
        print ("address"+str(i)+":", wallet_list[i])    
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
    return views