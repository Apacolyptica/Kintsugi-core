from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                  'kintsugi.views.index'),  # Index page
    url(r'^.+search\.py.*',	'kintsugi.views.search_request'), # Execute a search
    url(r'^search/$',           'kintsugi.views.search'), # Start a search
    url(r'^members/$',		'kintsugi.views.members'),# Project members
    url(r'^cwe/(?P<cwe>\d+)/', 	'kintsugi.views.id')      # Look up the CWE with this ID
  
    # Examples:
    # url(r'^$', 'kintsugi.views.home', name='home'),
    # url(r'^kintsugi/', include('kintsugi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


