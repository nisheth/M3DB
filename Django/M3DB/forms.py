from django import forms
from M3DB.models import *
from django.contrib.auth.models import User,Group
import csv,subprocess

class FastaForm(forms.Form):
  name = forms.CharField(required=False)
  fasta = forms.CharField(widget=forms.Textarea)

class ProjectForm(forms.ModelForm): 
  class Meta:
    model = Project
    fields = ('name','pi_name','e_mail','description')

class ExperimentForm(forms.ModelForm):
  class Meta:
    model = Experiment
    fields = ('project_id','name','date','platform', 'username','gene_region')
  #project = forms.ModelChoiceField(queryset = Project.objects.all())

class RegisterForm(forms.Form):
  username = forms.CharField()
  first_name = forms.CharField()
  last_name = forms.CharField()
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput)
  group = forms.ModelChoiceField(queryset=Group.objects.all())

  def clean(self):
    clean = super(RegisterForm, self).clean()

    username = clean.get("username")
    password = clean.get("password")
    password2 = clean.get("confirm_password")

    if username and User.objects.filter(username=username).exists():
      raise forms.ValidationError("Username '%s' is already taken. Please select another." % username)
    if password and password2:
   # Only run additional check if both are valid so far (valid here meaning not blank)
      if password != password2:
        raise forms.ValidationError("Passwords did not match. Please enter the same password in both fields.")
    return clean

class SampleForm(forms.ModelForm):
  class Meta:
    model = Sample
    fields = ('name','exp_id')
  file = forms.FileField()
  def csvparser(self,path):
    #objs = []
    samplename = self.cleaned_data['sample_name']
    expid = self.cleaned_data['exp_id']
    reader = csv.reader(path,delimiter='\t')
    for row in reader:
      _, created = Sample.objects.get_or_create(
            sample_id = row[5],
            name = samplename, #NOT IN FILE
            exp_name = expid, #NOT IN FILE
            index1 = row[2],
            index2 = row[4],
            #plate = row[0],
            #well = row[1],
    )
    #  objs.append(_)
    #Sample.objects.bulk_create(objs)
class ViewSampleForm(forms.ModelForm):
  def __init__(self,request,*args,**kwargs):
    try:
      super(ViewSampleForm, self).__init__(*args, **kwargs)
      self.fields['exp_id'].queryset = Experiment.objects.filter(project_id=request)
    except:
      pass
  class Meta:
    model = Sample
    fields = ('exp_id',)

class UploadReadsForm(forms.ModelForm):
  class Meta:
    model = UploadedFiles
    fields = ['forward_read','reverse_read']

class ViewSamplestatsForm(forms.ModelForm):
  def __init__(self,request,*args,**kwargs):
    super(ViewSamplestatsForm, self).__init__(*args, **kwargs)
    try:
      self.fields['exp_id'].queryset = SampleStatsitics.objects.filter(exp_id=request)
    except:
      pass
  class Meta:
    model = SampleStatistics
    fields = ('exp_id',)

class ViewAbundanceForm(forms.ModelForm):
  def __init__(self,request,*args,**kwargs):
    super(ViewAbundanceForm, self).__init__(*args, **kwargs)
    try:
      self.fields['exp_id'].queryset = AbundanceProfile.objects.filter(exp_id=request)
    except:
      pass
  class Meta:
    model = AbundanceProfile
    fields = ('exp_id',)

class ViewRAForm(forms.ModelForm):
  def __init__(self,request,*args,**kwargs):
    super(ViewRAForm, self).__init__(*args, **kwargs)
    try:
      self.fields['sample_id'].queryset = ReadAssignment.objects.filter(sample_id=request)
    except:
      pass
  class Meta:
    model = ReadAssignment
    fields = ('sample_id',)
