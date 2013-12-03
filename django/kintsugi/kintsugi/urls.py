from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                  'kintsugi.views.index'),  # index page
    url(r'^.+search\.py.*',	'kintsugi.views.search_request'),
    url(r'^search/$',           'kintsugi.views.search'), # start a search or return results
    url(r'^members/$',		'kintsugi.views.members'),
    url(r'^cwe/(?P<cwe>\d+)/', 	'kintsugi.views.id')      # look up the CWE with this ID
  
    # Examples:
    # url(r'^$', 'kintsugi.views.home', name='home'),
    # url(r'^kintsugi/', include('kintsugi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


