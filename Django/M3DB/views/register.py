from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from M3DB.forms import RegisterForm

def register(request):
  params = {}
  form = RegisterForm()
  if request.method == "POST":
    form = RegisterForm(request.POST)
    valid = form.is_valid()
    if valid:
      cd = form.cleaned_data
      username = cd['username']
      password = cd['password']
      first = cd['first_name']
      last = cd['last_name']
      email = cd['email']
   #   group = cd['group']
      user = User.objects.create_user(username,email=email,password=password)
      user.first_name = first
      user.last_name = last
      user.save()
      group.user_set.add(user)
      group.save()
      user = authenticate(username=username,password=password)
      return redirect('M3DB.home')
  params['form'] = form
  return render(request,'register.html',params)  
