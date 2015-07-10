#viewsamplestats.py
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from M3DB.models import *
from M3DB.decorators import *

@login_required
@activeexp
def viewSamplestats(request):
  params = {}
  searchdict = {}
  searchdict['exp_id'] = request.session['exp_id']
  results = SampleStatistics.objects.filter(**searchdict)
  params['results'] = results
  return render(request, 'viewSamplestats.html', params)
