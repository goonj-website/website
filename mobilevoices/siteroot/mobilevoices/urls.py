from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
#from haystack.forms import FacetedSearchForm
#from haystack.query import SearchQuerySet
#from haystack.views import FacetedSearchView
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#sqs = SearchQuerySet().facet('title')

#urlpatterns = patterns('haystack.views',
#    url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
#)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
  #  url(r'', include('gmapi.urls.media')),
    url(r'^$', 'mobilevoices.views.index'),
    url(r'^about$', 'mobilevoices.views.about'),
    url(r'^contact$', 'mobilevoices.views.contact'),
    url(r'^team$', 'mobilevoices.views.team'),
    url(r'^reports', 'mobilevoices.views.reports'),   
    url(r'^story/(?P<story_id>\d+)/$', 'mobilevoices.views.story'),
    url(r'^topic_channel/(?P<topic_channel_id>\d+)/$', 'mobilevoices.views.topic_channel'),
    url(r'^govt_dept/(?P<gd_id>\d+)/$', 'mobilevoices.views.govt_dept'),
    url(r'^channel_partner/(?P<channel_partner_id>\d+)/$', 'mobilevoices.views.channel_partner'),
    url(r'^community_rep/(?P<community_rep_id>\d+)/$', 'mobilevoices.views.community_rep'),
    url(r'^location/(?P<location_id>\d+)/$', 'mobilevoices.views.location'),
    url(r'^top10/$', 'mobilevoices.views.top10'),
    url(r'^issue/(?P<issue_id>\d+)/$', 'mobilevoices.views.issue'),
    url(r'^all_issues/', 'mobilevoices.views.all_issues'),
    url(r'^all_stories/', 'mobilevoices.views.all_stories'),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^search/', include('haystack.urls')),
    url(r'^events/', 'mobilevoices.views.timelines'), #FOR TESTING TIMELINES ONLY
    url(r'^campaigns/', 'mobilevoices.views.campaigns'), #FOR TESTING campaigns ONLY
    url(r'^maps/', 'mobilevoices.views.MAPS'),
    url(r'^capture/(?P<id>\d+)/$', 'mobilevoices.views.capture'),
)

#if settings.ENVIRONMENT==settings.ENV_DEVELOPMENT:
urlpatterns += patterns("django.views",
    url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {"document_root": settings.MEDIA_ROOT,})
)
