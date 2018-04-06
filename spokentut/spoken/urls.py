from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.log, name='log'),
    path('logout', auth_views.logout, {'next_page':'log'}, name='logout'),
    path('admindata', views.admindata, name='admindata'),
    path('userpg', views.userpg, name='userpg'),
]