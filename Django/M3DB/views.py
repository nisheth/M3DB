# # Create your views here.
# from django.shortcuts import render
# from M3DB.models import *
# from M3DB.forms import *
# def home(request):
#   return render(request, 'base.html')

# def createProject(request):
#   params = {}
#   form = ProjectForm()
#   if request.method=='POST':
#     form = ProjectForm(request.POST)
#     if form.is_valid():
#       form.save()
#       params['msg'] = "Project Created!"
#       form = ProjectForm()
#   params['form'] = form
#   return render(request, 'createProject.html', params)

# def viewProject(request):
#   params = {}
#   results = Register.objects.all()
#   params['results'] = results
#   return render(request, 'viewProject.html', params)

# def createExperiment(request):
#   params = {}
#   form = ExperimentForm()
#   if request.method == 'POST':
#     form = ExperimentForm(request.POST)
#     if form.is_valid():
#       form.save()
#       params['msg'] = "Experiment Created!"
#       form = ExperimentForm()
#   params['form'] = form
#   return render(request,'createExperiment.html', params)


# # def createSample(request):
# #   params = {}
# #   form = SampleForm()
# #   if request.method == 'POST':
# #     form = SampleForm(request.POST)
# #     if form.is_valid():
# #       form.save()
# #       params['msg'] = "Sample Created!"
# #       form = SampleForm()
# #   params['form'] = form
# #   return render(request, 'createSample.html', params)
