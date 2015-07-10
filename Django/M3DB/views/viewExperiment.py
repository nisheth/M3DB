from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from M3DB.models import *
from M3DB.decorators import *

@login_required
@activeproject
def viewExperiment(request):
    params = {}
    params['experiments'] = Experiment.objects.filter(project_id=request.session['project_id'])
    if request.method=='POST':
        expstring = request.POST.get('exp_id')
        request.session['exp_id'] = expstring
        messages.add_message(request, messages.SUCCESS, "Experiment changed to %s" % expstring)
        return redirect('viewSample')
    return render(request, 'viewExperiment.html', params)