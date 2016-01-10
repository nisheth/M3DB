from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from rest_framework import routers
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'M3DB.views.home.home', name='home'),
    url(r'^register/','M3DB.views.register.register',name='register'),
    url(r'login/','M3DB.views.login.main',name='login'),
    url(r'^logout/','M3DB.views.logout.main',name='logout'),
    # url(r'^M3DB/', include('M3DB.foo.urls')),
    url(r'^createProject/', 'M3DB.views.createProject.createProject', name='createProject'),
    url(r'^viewProject/','M3DB.views.viewProject.viewProject',name='viewProject'),
    url(r'^createExperiment/','M3DB.views.createExperiment.createExperiment',name='createExperiment'),
    url(r'^viewExperiment/','M3DB.views.viewExperiment.viewExperiment',name='viewExperiment'),
    url(r'^sample/','M3DB.views.sample.sample',name='sample'),
    url(r'^viewSample/','M3DB.views.viewSample.viewSample',name='viewSample'),
    url(r'^uploadReads/','M3DB.views.uploadReads.uploadReads',name='uploadReads'),
    #url(r'^analyzeReads/','M3DB.views.analyzeReads.analyzeReads',name='analyzeReads'),
    url(r'^viewSamplestats/','M3DB.views.viewSamplestats.viewSamplestats',name='viewSamplestats'),
    url(r'^viewAbundance/','M3DB.views.viewAbundance.viewAbundance',name='viewAbundance'),
    url(r'^viewReadAssign/','M3DB.views.viewReadAssign.viewReadAssign',name='viewReadAssign'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
from M3DB.views.api import * 
router = routers.DefaultRouter()
router.register(r'project',ProjectViewSet)
router.register(r'experiment',ExperimentViewSet)
router.register(r'sample',SampleViewSet)
router.register(r'samplestatistics',SampleStatisticsViewSet)
router.register(r'taxonomy',TaxonomyViewSet)
router.register(r'readassignment',ReadAssignmentViewSet)
router.register(r'abundanceprofile',AbundanceProfileViewSet)
router.register(r'analysis',AnalysisViewSet)
router.register(r'metadata',MetadataViewSet)
router.register(r'refdb',RefDbViewSet)

urlpatterns += patterns('',
    (r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
    (r'^api/', include(router.urls)),
    )
