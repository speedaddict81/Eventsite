from django.conf.urls import patterns, url
from events import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cats/$', views.cats, name='cats'),
    url(r'^search/$', views.search, name='search'),
    #url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
)
