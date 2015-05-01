from django.conf.urls import url

from .views import HelpPageView

urlpatterns = [
    url(r'^$', 'home.views.home', name='home'),
    url(r'^help/$', HelpPageView.as_view(), name='help'),
]
