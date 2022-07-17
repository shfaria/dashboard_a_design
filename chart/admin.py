from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render, redirect
from .models import Sales
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from numpy import row_stack
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine
# from .views import readfile

class SalesAdmin(admin.ModelAdmin):
    list_display = ('country', 'orderID', 'totalCost', 'category')
 
    def get_urls(self):
        urls = super().get_urls()
        new_url = [path('upload_csv/', self.upload_csv),]
        return new_url + urls


    def readfile(self, file):
        global data

        afile= pd.read_csv(file, sep='[:;,_|]', engine='python')
        print(afile)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format( user=user,password=password,database_name=database_name,)

        engine = create_engine(database_url)

        afile.to_sql(Sales._meta.db_table, con=engine, if_exists='append', index=False)
       

        


    def upload_csv(self, request):
        global attribute1

        if request.method == "POST":
            uploaded_file = request.FILES["document"]
            attribute1 = request.POST.get('attributeid')
            
            if uploaded_file.name.endswith('.csv'):

                savefile = FileSystemStorage()
                name = savefile.save(uploaded_file.name, uploaded_file)
                file_directory = os.getcwd() + '/media/' + name
                print(file_directory)

                self.readfile(file_directory)
                os.remove(file_directory)



                

                url = reverse('admin:index')
                return HttpResponseRedirect(url)

            else:
                messages.warning(request, 'cant upload file. please use csv format')
   

        form = UploadFileForm()
        data = {'form': form}

        return render(request, 'admin/upload_csv_page.html', data)


admin.site.register(Sales, SalesAdmin)