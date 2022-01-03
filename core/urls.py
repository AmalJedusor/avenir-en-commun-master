from django.urls import path, include
from django.conf.urls import url
from core import views
#from .views import MySearchView
from haystack.generic_views import SearchView
urlpatterns = [
    path('', views.home),
    path('sommaire', views.toc),
    path('chapitre/<slug:n>/<slug:slug>', views.chapter),
    path('section/<slug:n>/<slug:slug>', views.section),
    path('part/<slug:n>/<slug:slug>', views.part),
    path('hasard', views.random),
    path('fin/', views.fin),
    path('page/mentions-legales', views.mentions),
    path('recherche/', views.recherche),
    path('s<slug:n>',views.redirect_short),
    path('c<slug:n>',views.redirect_short)  
]
