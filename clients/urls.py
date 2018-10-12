
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^showAll/$', views.showClients, name='showClients'),
    url(r'^extend/', views.extendClient, name='extendClients'),
    url(r'^shorten/', views.shortenClient, name='extendClients'),
    url(r'^createInvoices/', views.createInvoices, name='createInvoices'),
    url(r'^edit/(?P<client_id>\d+)/$', views.edit, name='createInvoices'),
]
