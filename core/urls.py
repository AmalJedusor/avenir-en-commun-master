from django.urls import path, re_path
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
    path('c<n>/',views.redirect_short),



    re_path(r'^s(?P<n>[0-9]{1,2})/$',views.redirect_short),
    re_path(r'^s(?P<n>[0-9]{1,2})m(?P<m>[0-9]{1,3})/$',views.redirect_short_measure),
    path('c<slug:n>',views.redirect_short),
    path('visuel/<slug:v>', views.visuel),
    path('grid',views.grid),
    path('grid/<int:p>',views.grid_page)
]
