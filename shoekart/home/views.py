from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def index(request):
    if 'email' in request.session:
        return render(request, 'home/index.html')
    return redirect('user_login')


def about(request):
    return render(request, 'home/about.html')
