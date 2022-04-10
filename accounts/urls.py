from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # User Register/Login
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    # User Vertification
    path('activate-user/', views.activateUser, name='activate-user'),
    path('activate/<uidb64>/<token>', views.VertificationView.as_view(), name='activate'),

    # User Profile CRUD
    path('profile/', views.userProfile, name='userProfile'),
    path('profile/edit/', views.userUpdate, name='userUpdate'),
    path('profile/change-password/', views.userUpdatePassword, name='userUpdatePassword'),

    # Reset Password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/reset-password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset-password-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset-password-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset-password-complete.html'), name='password_reset_complete'),

]