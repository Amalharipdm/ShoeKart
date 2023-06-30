from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Create your views here.
@never_cache
@login_required(login_url='user_login')
def index(request):
    if 'email' in request.session:
        return render(request, 'home/index.html')
    return redirect('user_login')

def search(request):
    if request.method == 'POST':
        search_value = request.POST.get('search', '')
        print('search_value:',search_value)
        return {'search': search_value}
    else:
        return {'search': ''}


def about(request):
    return render(request, 'home/about.html')
