#sample profile
import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from M3DB.models import *
from M3DB.forms import *

@login_required
def sample(request):
	samplename = form['sample_name']
	expid = form['exp_id']
	with open(path) as f:
		reader = csv.reader(f)
		for row in reader:
		_, created = Sample.objects.get_or_create(
			sample_id = row[5],
            sample_name = samplename, #NOT IN FILE
            exp_id = expid, #NOT IN FILE
            index1 = row[2],
            index2 = row[4],
            plate = row[0],
            well = row[1],
		)
		_.save()