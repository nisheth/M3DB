from M3DB.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment

class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sample

class SampleStatisticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleStatistics

class TaxonomySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxonomy

class ReadAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReadAssignment

class AbundanceProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AbundanceProfile

class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Analysis

class MetadataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metadata

class RefDbSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RefDb
