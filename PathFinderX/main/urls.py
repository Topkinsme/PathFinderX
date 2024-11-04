from django.urls import path

from . import views

urlpatterns=[
    path("",views.home,name='Home'),
    path('find-shortest-path/', views.find_shortest_path, name='find_shortest_path'),
]