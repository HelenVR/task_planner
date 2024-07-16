from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


# urlpatterns = [
#        path('register/', views.register, name='register'),
#        path('login/', views.user_login, name='login'),
#        path('tasks/', views.task_list, name='tasks'),
#        path('tasks/new/', views.task_create, name='task_create'),
#        path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
#        path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
#    ]

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
]