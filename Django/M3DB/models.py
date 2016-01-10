# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UploadedFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    forward_read = models.CharField(max_length=100)
    reverse_read = models.CharField(max_length=100)
    class Meta:
        db_table = 'M3DB_uploadedfiles'

class AbundanceProfile(models.Model):
    profile_id = models.IntegerField(primary_key=True)
    exp_id = models.ForeignKey('Experiment',null=False,db_column='exp_id',to_field='exp_id',blank=True)
    sample_id = models.ForeignKey('Sample',null=False,db_column='sample_id',to_field='sample_id',blank=True)
    analysis = models.ForeignKey('Analysis', null=True, blank=True)
    taxonomy = models.ForeignKey('Taxonomy', null=True, blank=True)
    num_reads = models.IntegerField(null=True, blank=True)
    abundance = models.FloatField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=2, blank=True)
    miscellaneous = models.CharField(max_length=1000, blank=True)
    taxonomy_level = models.CharField(max_length=1000, blank=True)
    taxonomy_name = models.CharField(max_length=1000, blank=True)
    class Meta:
        db_table = 'abundance_profile'

class Analysis(models.Model):
    analysis_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1000)
    parameters = models.CharField(max_length=256)
    comments = models.CharField(max_length=500)
    refdb = models.ForeignKey('RefDb')
    class Meta:
        db_table = 'analysis'

# class AuthGroup(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=80)
#     class Meta:
#         db_table = 'auth_group'

# class AuthGroupPermissions(models.Model):
#     id = models.IntegerField(primary_key=True)
#     group = models.ForeignKey(AuthGroup)
#     permission = models.ForeignKey('AuthPermission')
#     class Meta:
#         db_table = 'auth_group_permissions'

# class AuthPermission(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     content_type = models.ForeignKey('DjangoContentType')
#     codename = models.CharField(max_length=100)
#     class Meta:
#         db_table = 'auth_permission'

# class AuthUser(models.Model):
#     id = models.IntegerField(primary_key=True)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField()
#     is_superuser = models.BooleanField()
#     username = models.CharField(max_length=30,unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.CharField(max_length=75)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()
#     def __unicode__(self):
#         return self.username
#     class Meta:
#         db_table = 'auth_user'

# class AuthUserGroups(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user = models.ForeignKey(AuthUser)
#     group = models.ForeignKey(AuthGroup)
#     class Meta:
#         db_table = 'auth_user_groups'

# class AuthUserUserPermissions(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user = models.ForeignKey(AuthUser)
#     permission = models.ForeignKey(AuthPermission)
#     class Meta:
#         db_table = 'auth_user_user_permissions'

# class DjangoAdminLog(models.Model):
#     id = models.IntegerField(primary_key=True)
#     action_time = models.DateTimeField()
#     user = models.ForeignKey(AuthUser)
#     content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
#     object_id = models.TextField(blank=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     class Meta:
#         db_table = 'django_admin_log'

# class DjangoContentType(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=100)
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#     class Meta:
#         db_table = 'django_content_type'

# class DjangoSession(models.Model):
#     session_key = models.CharField(max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#     class Meta:
#         db_table = 'django_session'

# class DjangoSite(models.Model):
#     id = models.IntegerField(primary_key=True)
#     domain = models.CharField(max_length=100)
#     name = models.CharField(max_length=50)
#     class Meta:
#         db_table = 'django_site'

class Project(models.Model):
    project_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=1000, unique=True, blank=True)
    pi_name = models.CharField(max_length=1000, blank=True)
    e_mail = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    username = models.CharField(max_length=30,blank=True,null=True)#ForeignKey(AuthUser, null=True, db_column='username', to_field='username', blank=True)
    authorized = models.CharField(max_length=1000,null=True,blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'project'

class Experiment(models.Model):
    exp_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, blank=True)
    date = models.DateField(null=True, blank=True)
    platform = models.CharField(max_length=100, blank=True)
    gene_region = models.CharField(max_length=10, blank=True)
    username = models.CharField(max_length=30,blank=True,null=True)#ForeignKey(AuthUser, null=True, db_column='username', to_field='username', blank=True)
    project_id = models.ForeignKey('Project',null=True,db_column='project_id',to_field='project_id',blank=False)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'experiment'

class Metadata(models.Model):
    id = models.IntegerField(primary_key=True)
    sample_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    class Meta:
        db_table = 'metadata'


class RefDb(models.Model):
    refdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=1000)
    version = models.CharField(max_length=256)
    class Meta:
        db_table = 'ref_db'

class Sample(models.Model):
    sample_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=1000, blank=True)
    index1 = models.CharField(max_length=20,blank=True) #models.ForeignKey(Experiment, null=True, db_column='index1', blank=True)
    index2 = models.CharField(max_length=20, blank=True)
    exp_id = models.ForeignKey('Experiment',null=False,db_column='exp_id',to_field='exp_id',blank=False)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'sample'

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
    exp_id = models.ForeignKey('Experiment',null=False,db_column='exp_id',to_field='exp_id',blank=False)
    sample_id = models.ForeignKey('Sample',null=False,db_column='sample_id',to_field='sample_id',blank=True, primary_key=True)
    class Meta:
        db_table = 'sample_statistics'

class Taxonomy(models.Model):
    tax_id = models.IntegerField(primary_key=True)
    tax_name = models.TextField()
    tax_level = models.TextField()
    refdb = models.ForeignKey(RefDb)
    parent_id = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=20)
    class Meta:
        db_table = 'taxonomy'

class ReadAssignment(models.Model):
    exp_id = models.ForeignKey('Experiment',null=False,db_column='experiment_id',to_field='exp_id',blank=False)
    sample_id = models.ForeignKey(Sample,null=True,db_column='sample_id',to_field='sample_id',blank=False)
    read_id = models.CharField(max_length=1000,primary_key=True)
    taxonomy_id = models.IntegerField(null=True,blank=True)
    taxonomy_name = models.CharField(max_length=1000,blank=True)
    taxonomy_level = models.CharField(max_length=1000,blank=True)
    score = models.FloatField(null=True,blank=True)
    analysis_id = models.ForeignKey(Analysis,null=True,db_column='analysis_id',to_field='analysis_id',blank=True)
    status = models.CharField(max_length=2,blank=False)
    misc = models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        managed = False
        db_table = 'read_assignment'
