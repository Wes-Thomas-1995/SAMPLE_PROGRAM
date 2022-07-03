
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect




def Home_Page(request):
    return render(request, 'home/home-page.html')


