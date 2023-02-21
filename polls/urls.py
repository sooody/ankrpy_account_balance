# -*- mode: python ; coding: utf-8 -*-
from django.urls import path, re_path
from . import views
from . import exportin

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('send_addr/',views.one_wallet),
    path('upload/', exportin.handle_upload),
]