from django.conf.urls import patterns, include, url
from tastypie.api import Api
from blog.api import PostResource, CmtResource, UserResource, TagResource, SearchResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(PostResource())
v1_api.register(CmtResource())
v1_api.register(UserResource())
v1_api.register(TagResource())
v1_api.register(SearchResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tpblog.views.home', name='home'),
    url('^blog/', include('blog.urls')),
    url(r'^tasty/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
