from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import connection
from django.contrib.auth import authenticate, login
import sqlite3
from datetime import datetime
from sqlite3 import Error


from django.apps import apps 
from django.contrib import admin 
from django.contrib.admin.sites import AlreadyRegistered 

from .models import Msg


def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(db_file)
    except Error as e:
        print(e)

    return conn

# Create your views here.
# @csrf_exempt
@login_required
def index(request):
        messages = Msg.objects.filter(Q(source=request.user) | Q(target=request.user))
        users = User.objects.exclude(pk=request.user.id)
        return render(request, 'messaging_app/index.html', {'msgs': messages, 'users': users})

@csrf_protect
def signupView(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.create_user(username=username,password=password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    

    return render(request, 'messaging_app/signup.html')

@login_required
def addView(request):
        target = User.objects.get(username=request.POST.get('to'))
        # Msg.objects.create(source=request.user, target=target, 
        #     content=request.POST.get('content'))
        # sql="INSERT INTO messaging_app_msg (source_id,target_id,content,time) VALUES (?, ?, ?, ?)"
        # sql="INSERT INTO messaging_app_msg VALUES (?,?,?,?)"
        
        # vals=[(request.user.id), (target.id), (request.POST.get('content')),datetime.now()]

        # app_models = apps.get_app_config('messaging_app').get_models()
        # for m in app_models:
        #     print(m)
        # print(Msg._meta.db_table)
        sql="INSERT INTO messaging_app_msg (time,content,source_id,target_id) VALUES " + "('" + str(datetime.now()) + "','" + str(request.POST.get('content')) + "','" + str(request.user.id) +"','" + str(target.id) + "');"
        connection = create_connection('db.sqlite3')
        cursor=connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

        query=Msg.objects.raw("SELECT * FROM messaging_app_msg")
        for q in query:
            print("time ",q.time)
            print("content ",q.content)
            print("source_id ",q.source_id)
            print("target_id ",q.target_id)
            

        return redirect('/')



def settingsView(request):
    return render(request,'messaging_app/settings')