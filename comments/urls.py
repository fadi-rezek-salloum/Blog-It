from django.urls import path

from . import views

urlpatterns = [

    # Comment CRUD
    path('update-comment/<str:pk>', views.updateComment, name='update-comment'),
    path('delete-comment/<str:pk>', views.deleteComment, name='delete-comment'),

]