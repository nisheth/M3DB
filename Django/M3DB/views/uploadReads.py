#uploadReads.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from M3DB.models import *
from M3DB.forms import UploadReadsForm

@login_required
def uploadReads(request):
	params = {}
	form = UploadReadsForm()
	if request.method == 'POST':
		form = UploadReadsForm(request.POST,request.FILES)
		if form.is_valid():
                        form.save()
                        #form.readsparser(request.FILES['reverse_read'])
			params['msg'] = "Analysis has begun!"
			form = UploadReadsForm()
	params['form'] = form
	return render(request,'uploadReads.html',params)
