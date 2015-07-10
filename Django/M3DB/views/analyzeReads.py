# #uploadReads.py
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render,redirect
# from M3DB.models import *
# from M3DB.forms import AnalyzeReadsForm

# @login_required
# def analyzeReads(request):
#         params = {}
#         form = AnalyzeReadsForm()
#         if request.method == 'POST':
#                 form = AnalyzeReadsForm(request.POST)
#                 if form.is_valid():
#                         cd = form.cleaned_data
#                         form.ReadsProcessor(cd['samples_file_set'],cd['meep'],cd['save_nonoverlap'],cd['patch_length'])
#                         #form.readsparser(request.FILES['reverse_read'])
#                         params['msg'] = "Analysis has begun!"
#                         form = AnalyzeReadsForm()
#         params['form'] = form
#         return render(request,'analyzeReads.html',params)
