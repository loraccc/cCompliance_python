from django.urls import path
from . import views

urlpatterns = [
    path('sections/', views.section_list, name='section_list'),
    path('section/create/', views.section_create, name='section_create'),
    path('section/update/<int:pk>/', views.section_update, name='section_update'),
    path('section/delete/<int:pk>/', views.section_delete, name='section_delete'),
]
