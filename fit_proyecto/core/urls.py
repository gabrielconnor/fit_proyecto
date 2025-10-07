from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('create/', views.entry_create, name='entry_create'),
    path('delete/<int:pk>/', views.entry_delete, name='entry_delete'),
    path('edit/<int:pk>/', views.entry_update, name='entry_update'),    
]