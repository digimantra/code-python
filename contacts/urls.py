from django.conf.urls import url
from . import views


app_name = 'contacts'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^subscribe/$', views.SubscribeEmailPageView.as_view(), name='subscribe'),
]
