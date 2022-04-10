from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='index'),
    # Contact us Page
    path('contact/', views.contact, name='contact'),
    # All Articles
    path('articles/', views.articlesList, name='articles'),
]