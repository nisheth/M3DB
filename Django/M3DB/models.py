from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UploadedFiles(models.Model):
    forward_read = models.CharField(max_length=100)
    reverse_read = models.CharField(max_length=100)

class AbundanceProfile(models.Model):
    exp_id = models.ForeignKey(Experiment)
    sample_id = models.ForeignKey(Sample)
    analysis = models.ForeignKey('Analysis', null=True, blank=True)
    taxonomy = models.ForeignKey('Taxonomy', null=True, blank=True)
    num_reads = models.IntegerField(null=True, blank=True)
    abundance = models.FloatField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=2, blank=True)
    miscellaneous = models.CharField(max_length=1000, blank=True)
    taxonomy_level = models.CharField(max_length=1000, blank=True)
    taxonomy_name = models.CharField(max_length=1000, blank=True)

class Analysis(models.Model):
    analysis_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000)
    parameters = models.CharField(max_length=256)
    comments = models.CharField(max_length=500)
    refdb = models.ForeignKey(RefDb)

class Project(models.Model):
    name = models.CharField(max_length=1000, unique=True, blank=True)
    pi_name = models.CharField(max_length=1000, blank=True)
    e_mail = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    username = ForeignKey(User, null=True, db_column='username', to_field='username', blank=True)
    authorized = models.CharField(max_length=1000,null=True,blank=True)
    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True)
    date = models.DateField(null=True, blank=True)
    platform = models.CharField(max_length=100, blank=True)
    gene_region = models.CharField(max_length=10, blank=True)
    username = models.CharField(max_length=30,blank=True,null=True)#ForeignKey(AuthUser, null=True, db_column='username', to_field='username', blank=True)
    project_id = models.ForeignKey(Project)
    def __unicode__(self):
        return self.name

class Metadata(models.Model):
    sample_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


class RefDb(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    version = models.CharField(max_length=256)

class Sample(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    index1 = models.CharField(max_length=20,blank=True)
    index2 = models.CharField(max_length=20, blank=True)
    exp_id = models.ForeignKey(Experiment)
    def __unicode__(self):
        return self.name

class SampleStatistics(models.Model):
    total_reads = models.IntegerField(null=True, blank=True)
    overlapping_reads = models.IntegerField(null=True, blank=True)
    per_overlapping_reads = models.FloatField(null=True, blank=True)
    non_overlapping_reads = models.IntegerField(null=True, blank=True)
    per_non_overlapping_reads = models.FloatField(null=True, blank=True)
    avg_read_length = models.FloatField(null=True, blank=True)
    avg_quality = models.FloatField(null=True, blank=True)
    avg_mee = models.FloatField(null=True, blank=True)
    meep_cutoff = models.FloatField(null=True, blank=True)
    hq_reads = models.IntegerField(null=True, blank=True)
    per_hq_reads = models.FloatField(null=True, blank=True)
    per_hq_overlap_reads = models.FloatField(null=True, blank=True)
    hq_avg_length = models.FloatField(null=True, blank=True)
    hq_avg_quality = models.FloatField(null=True, blank=True)
    hq_avg_mee = models.FloatField(null=True, blank=True)
    exp_id = models.ForeignKey(Experiment)
    sample_id = models.ForeignKey(Sample)

class Taxonomy(models.Model):
#    tax_id = models.IntegerField(primary_key=True)
    tax_name = models.TextField()
    tax_level = models.TextField()
    refdb = models.ForeignKey(RefDb)
    parent_id = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=20)

class ReadAssignment(models.Model):
    exp_id = models.ForeignKey(Experiment)
    sample_id = models.ForeignKey(Sample)
    read_id = models.CharField(max_length=1000,primary_key=True)
    taxonomy_id = models.IntegerField(null=True,blank=True)
    taxonomy_name = models.CharField(max_length=1000,blank=True)
    taxonomy_level = models.CharField(max_length=1000,blank=True)
    score = models.FloatField(null=True,blank=True)
    analysis_id = models.ForeignKey(Analysis)
    status = models.CharField(max_length=2,blank=False)
    misc = models.CharField(max_length=1000,null=True,blank=True)
