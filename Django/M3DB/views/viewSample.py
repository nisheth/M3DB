#viewSample.py Page
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from M3DB.models import *
from M3DB.decorators import *
@login_required
@activeexp
def viewSample(request):
  params = {}
  searchdict = {}
  searchdict['exp_id'] = request.session['exp_id']
  results = Sample.objects.filter(**searchdict)
  params['results'] = results
  return render(request, 'viewSample.html', params)