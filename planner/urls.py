from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/edit/<int:pk>/', views.subject_edit, name='subject_edit'),
    path('subjects/delete/<int:pk>/', views.subject_delete, name='subject_delete'),
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/add/', views.task_add, name='task_add'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('tasks/complete/<int:pk>/', views.task_complete, name='task_complete'),
    path('tasks/pending/<int:pk>/', views.task_pending, name='task_pending'),
    path('profile/', views.profile_view, name='profile'),
]
