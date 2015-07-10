#viewReadAssign.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.db.models import Count
from django.http import JsonResponse,HttpResponse
from M3DB.models import *
from M3DB.forms import ViewRAForm
from M3DB.decorators import *

@login_required
@activeexp
def viewReadAssign(request):
  params = {}
  if request.method == "POST":
    params['form'] = ViewRAForm(request.session['exp_id'],request.POST)
    if params['form'].is_valid():
      cd = params['form'].cleaned_data
      searchdict = {}
      searchdict['sample_id'] = cd['sample_id']
      results = ReadAssignment.objects.filter(**searchdict)[:100] \
        .values('taxonomy_name') \
        .annotate(count_items=Count('taxonomy_name'))
      params['results'] = results
      return JsonResponse(list(results),safe=False)
  else:
    params['form'] = ViewRAForm(request.session['exp_id'])
  return render(request, 'viewReadAssignment.html', params)
