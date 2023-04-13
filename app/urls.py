from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logout, name='logout'),
    path('info', views.info, name='info'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add-task', views.add_task, name='add-task'),
    path('add-goal', views.add_goal, name='add-goal'),
]