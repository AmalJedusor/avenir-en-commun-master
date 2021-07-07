from django.urls import path
from core import views

urlpatterns = [
    path('', views.home),
    path('sommaire/', views.toc),
    path('chapitre/<slug:n>/<slug:slug>', views.chapter),
    path('section/<slug:n>/<slug:slug>', views.section),
    path('hasard', views.random),
    path('recherche', views.search),
]
