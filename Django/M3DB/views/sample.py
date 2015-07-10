#sample upload page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from M3DB.models import *
from M3DB.forms import SampleForm

@login_required
def sample(request):
	params = {}
	form = SampleForm()
	if request.method == 'POST':
		form = SampleForm(request.POST,request.FILES)
		if form.is_valid():
			form.csvparser(request.FILES['file'])
			params['msg'] = "Upload and Save Successful!"
	params['form'] = form
	return render(request,'sample.html',params)
