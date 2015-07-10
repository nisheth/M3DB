from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from M3DB.models import *

@csrf_exempt
def main(request):
  username,password,mynext,firstname= '','','',''
  mynext = request.GET.get('next') or None
  if mynext is None: mynext  = 'viewProject'
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    mynext = request.POST.get('next') or None
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        #proj = Project.objects.get_or_none(user=user)
        return redirect(mynext)
  params = {
        'username' : username,
        'firstname': firstname,
        'next': mynext,
    }
  return render(request, 'login.html', params)
