# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Only include your custom register view here
    path('register/', views.register_user, name='register'),

    # REMOVE THESE LINES:
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
]