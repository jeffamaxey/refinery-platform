'''
Created on Feb 20, 2012

@author: nils
'''


from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from constants import UUID_RE

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(
        f'^data_sets/(?P<data_set_uuid>{UUID_RE})/$',
        views.data_set,
        name='data_set',
    ),
    url(
        r'^data_sets/(?P<slug>[a-zA-Z0-9\_]+)/$',
        views.data_set_slug,
        name='data_set_slug',
    ),
    url(r'^doi/(?P<id>.+)/', views.doi, name='doi'),
    url(f'^groups/(?P<query>{UUID_RE})/$', views.group, name='group'),
    url(
        f'^group_invite/(?P<token>{UUID_RE})/$',
        views.group_invite,
        name='group_invite',
    ),
    url(
        r'^pubmed/abstract/(?P<id>.+)/',
        views.pubmed_abstract,
        name='pubmed_abstract',
    ),
    url(
        r'^pubmed/search/(?P<term>.+)/',
        views.pubmed_search,
        name='pubmed_search',
    ),
    url(
        r'^pubmed/summary/(?P<id>.+)/',
        views.pubmed_summary,
        name='pubmed_summary',
    ),
    url(
        r'^sitestatistics/(?P<type>(deltas)|(totals)).csv',
        views.site_statistics,
    ),
    url(
        r'^solr/core/select/$', views.solr_core_search, name='solr_core_search'
    ),
    url(r'^users/(?P<query>[\@\.\-\+a-z0-9]+)/$', views.user),
    url(f'^users/(?P<query>{UUID_RE})/$', views.user, name='user'),
    url(
        f'^users/(?P<uuid>{UUID_RE})/edit/$', views.user_edit, name='user_edit'
    ),
    url(f'^workflows/(?P<uuid>{UUID_RE})/$', views.workflow, name='workflow'),
    url(
        r'^workflows/(?P<slug>[a-zA-Z0-9\_]+)/$',
        views.workflow_slug,
        name='workflow_slug',
    ),
]

router = DefaultRouter()
router.register(r'data_sets', views.DataSetViewSet, 'data_sets')
router.register(r'groups', views.GroupViewSet, 'groups')
router.register(r'invitations', views.InvitationViewSet, 'invitations')
router.register(r'workflows', views.WorkflowViewSet, 'workflows')

core_api_urls = router.urls + [
    url(r'^analyses/$', views.AnalysisAPIView.as_view()),
    url(r'^events/$', views.EventAPIView.as_view()),
    url(
        f'^user_profile/(?P<uuid>{UUID_RE})/$',
        views.UserProfileAPIView.as_view(),
    ),
    url(f'^analyses/(?P<uuid>{UUID_RE})/$', views.AnalysisAPIView.as_view()),
    url(
        r'^openid_token/$',
        views.OpenIDTokenAPIView.as_view(),
        name='openid-token',
    ),
    url(r'^obtain-auth-token/', views.ObtainAuthTokenValidSession.as_view()),
    url(r'^site_profiles/$', views.SiteProfileAPIView.as_view()),
]
