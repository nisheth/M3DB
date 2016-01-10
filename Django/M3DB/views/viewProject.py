from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from M3DB.models import *

@login_required
def viewProject(request):
    params = {}
    params['projects'] = Project.objects.filter(authorized__contains=request.user)
    if request.method=='POST':
        projectstring = request.POST.get('project__id')
        request.session['project_id'] = projectstring
        messages.add_message(request, messages.SUCCESS, "Project changed to %s" % projectstring)
        return redirect('viewExperiment')
    return render(request, 'viewProject.html', params)
