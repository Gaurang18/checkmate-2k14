from django.conf.urls import patterns, include, url
from checkmate.main.views import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'checkmate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',main,name='main'),
    url(r'^question/$',question,name='question'),
    url(r'^login/$',login,name='login'),
    url(r'^rulebook/$',rulebook,name='rulebook'),
    url(r'^transition/$',transition,name='transition'),
    url(r'^market/$',market,name='market'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^register/$',register,name='register'),
)

'''urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )'''

from settings import MEDIA_URL, MEDIA_ROOT, DEBUG
if DEBUG:
    #urlpatterns=patterns('',url(r'^2014/', include(urlpatterns)))
    from django.views.static import serve
    _media_url = MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': MEDIA_ROOT}))
    del(_media_url, serve)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )