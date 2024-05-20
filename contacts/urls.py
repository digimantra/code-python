from django.conf.urls import url
from . import views


app_name = 'contacts'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^thank-you/$', views.ThankYouView.as_view(), name='thank_you'),
    url(r'^subscribe-for-smart-strategies/$', views.SubscribePageView.as_view(), name='subscribe_for_smart_strategies'),
    url(r'^subscribe/$', views.SubscribeEmailPageView.as_view(), name='subscribe'),
]
