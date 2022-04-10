from django.urls import path

from . import views

urlpatterns = [
    # Article CRUD
    path('article-detail/<str:pk>', views.postDetail, name='article-detail'),
    path('article-create/', views.postCreate, name='article-create'),
    path('article-update/<str:pk>', views.postUpdate, name='article-update'),
    path('article-delete/<str:pk>', views.postDelete, name='article-delete'),

    # Search By Tags
    path('tag/<str:tag>/', views.tagArticles, name='tag-articles'),

]