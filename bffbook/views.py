from django.shortcuts import render

def home(request):
    user = request.user
    return render(request, 'main/home.html', {
        'user': user,
    })