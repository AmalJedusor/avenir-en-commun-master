from django.urls import path, include
from django.conf.urls import url
from core import views
#from .views import MySearchView
from haystack.generic_views import SearchView
urlpatterns = [
    path('', views.home),
    path('sommaire/', views.toc),
    path('chapitre/<slug:n>/<slug:slug>', views.chapter),
    path('section/<slug:n>/<slug:slug>', views.section),
    path('hasard', views.random),

    path('search/', views.search),
   
   
]
