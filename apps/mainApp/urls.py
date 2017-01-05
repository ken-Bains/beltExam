from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^new$', views.newUser),
    url(r'^signOn$', views.signOn),
    url(r'^success$', views.success),
    url(r'^addQuote$', views.add_quote),
    url(r'^user/(?P<id>\d+)$', views.add_to_fav),
    url(r'^remove_fav/(?P<id>\d+)$', views.remove_fav),
    url(r'^user_page/(?P<id>\d+)$', views.user_page),
    url(r'^logout$', views.logout),


]
