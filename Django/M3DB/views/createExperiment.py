from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from M3DB.models import *
from M3DB.forms import *

@login_required
def createExperiment(request):
  params = {}
  #something = dir(request.user)
  form = ExperimentForm(initial={'user':request.user})
  if request.method == 'POST':
    form = ExperimentForm(request.POST)
    if form.is_valid():
      savevar = form.save()
      params['msg'] = "Experiment Created! (%d)" % savevar.exp_id
      form = ExperimentForm()
  params['form'] = form
  return render(request,'createExperiment.html', params)
