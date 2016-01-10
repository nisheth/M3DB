from M3DB.serializers import *
from rest_framework import viewsets

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = ['id']

class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    filter_fields = ['id']

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_fields = ['id']

class SampleStatisticsViewSet(viewsets.ModelViewSet):
    queryset = SampleStatistics.objects.all()
    serializer_class = SampleStatisticsSerializer
    filter_fields = ['id']

class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer
    filter_fields = ['id']

class ReadAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ReadAssignment.objects.all()
    serializer_class = ReadAssignmentSerializer
    filter_fields = ['id']

class AbundanceProfileViewSet(viewsets.ModelViewSet):
    queryset = AbundanceProfile.objects.all()
    serializer_class = AbundanceProfileSerializer
    filter_fields = ['id']

class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    filter_fields = ['id']

class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    filter_fields = ['id']

class RefDbViewSet(viewsets.ModelViewSet):
    queryset = RefDb.objects.all()
    serializer_class = RefDbSerializer
    filter_fields = ['id']