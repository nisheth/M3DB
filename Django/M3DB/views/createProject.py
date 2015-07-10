from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from M3DB.models import *
from M3DB.forms import *

@login_required
def createProject(request):
  params = {}
  form = ProjectForm()
  if request.method=='POST':
    form = ProjectForm(request.POST)
    if form.is_valid():
      form.save()
      params['msg'] = "Project Created!"
      form = ProjectForm()
  params['form'] = form
  return render(request, 'createProject.html', params)

