from M3DB.serializers import *
from rest_framework import viewsets

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    

class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    

class SampleStatisticsViewSet(viewsets.ModelViewSet):
    queryset = SampleStatistics.objects.all()
    serializer_class = SampleStatisticsSerializer
    

class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer
    

class ReadAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ReadAssignment.objects.all()
    serializer_class = ReadAssignmentSerializer
    

class AbundanceProfileViewSet(viewsets.ModelViewSet):
    queryset = AbundanceProfile.objects.all()
    serializer_class = AbundanceProfileSerializer
    

class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    

class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    

class RefDbViewSet(viewsets.ModelViewSet):
    queryset = RefDb.objects.all()
    serializer_class = RefDbSerializer
    