from django.shortcuts import render,redirect

def home(request):
    user = request.user
    return redirect('login')