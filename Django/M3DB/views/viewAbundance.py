#viewabundance.py
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from M3DB.models import *
from M3DB.decorators import *

@login_required
@activeexp
def viewAbundance(request):
  params = {}
  searchdict = {}
  searchdict['exp_id'] = request.session['exp_id']
  apresults = AbundanceProfile.objects.filter(**searchdict)
  paginator = Paginator(apresults,275)
  page = request.GET.get('page')
  try:
  	results = paginator.page(page)
  except PageNotAnInteger:
  	results = paginator.page(1)
  except EmptyPage:
  	results = paginator.page(paginator.num_pages)
  params['results'] = results
  return render(request, 'viewAbundance.html', params)