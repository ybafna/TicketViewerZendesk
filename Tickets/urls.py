from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<ticket_id>[0-9]+)/$', views.get_individual_ticket, name="get_ticket"),
    path('', views.get_tickets, name='index'),

]
