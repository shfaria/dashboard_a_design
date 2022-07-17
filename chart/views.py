from multiprocessing import context
from typing import Counter
from attr import attributes
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from numpy import row_stack
import pandas as pd
from .models import Sales
from .admin import *



def home(request):
    all = Sales.objects.values_list('category', flat=True)
    country = list(all)
    dashboard = []

    for x in country:
        dashboard.append(x)
 
    dashboard1 = dict(Counter(dashboard))
    print(dashboard1)
    keys =  dashboard1.keys()
    values = dashboard1.values()
    print(keys)
    print(values)

    listkeys = list(keys)
    listvalues = list(values)
    
    context = {
        'listkeys': listkeys,
        'listvalues': listvalues,
    }




    return render(request, 'chart/home.html', context)




