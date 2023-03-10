from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.urls import reverse_lazy
# Create your views here.


def signup(request):
    form=SignUpForm()
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('main_post_view')
    form=SignUpForm()
    return render(request,'signup.html',{
        'form':form
    })

