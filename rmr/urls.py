from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic.simple import direct_to_template

from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       
     url(r'^admin/', include(admin.site.urls)),
     url(r'^books/', include('books.urls')),
     url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
)

urlpatterns += patterns('',               

    url(r'^login_form_ajax/$', direct_to_template, {'template': 'users/login_form.html'}, name='login_form_ajax'),  
        

)

#urlpatterns += patterns('django.contrib.auth.views',               
#
#    url(r'^login/$', 'login', {'template_name': 'users/login.html',}, name='login'),  
#    url(r'^logout/$', 'logout', {'template_name': 'users/login.html'},name='logout'),
#        
#
#)

if settings.SERVE_MEDIA:
    
    urlpatterns += staticfiles_urlpatterns()
