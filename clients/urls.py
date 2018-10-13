
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^showAll/$', views.showClients, name='showClients'),
    url(r'^showServices/$', views.showServices, name='showServices'),
    url(r'^showCompanys/$', views.showCompanys, name='showCompanys'),
    url(r'^extend/', views.extendClient, name='extendClients'),
    url(r'^shorten/', views.shortenClient, name='extendClients'),
    url(r'^createInvoices/', views.createInvoices, name='createInvoices'),
    url(r'^edit/(?P<client_id>\d+)/$', views.edit, name='createInvoices'),
    url(r'^editService/(?P<client_id>\d+)/$', views.editServices),
    url(r'^editCompany/(?P<client_id>\d+)/$', views.editCompany, ),
    url(r'^delCompany/(?P<company_id>\d+)/$', views.delCompany),
    url(r'^delService/(?P<service_id>\d+)/$', views.delService),
    url(r'^delClients/(?P<data_id>\d+)/$', views.delData),
    url(r'^addservice/$',views.addservice,name='addService'),
    url(r'^addcompany/$',views.addcompany,name='addCompany'),
    url(r'^addclient/$',views.addclient,name='addClient'),
]
