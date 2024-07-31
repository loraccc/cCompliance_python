from django.contrib import admin
from django.urls import path

from . import views

from .views import (list_users,get_user_permissions, user_create, user_update, user_delete,
                     role_list, role_create, role_update, role_delete,
                       register, user_login, user_logout,
                        admin_dashboard, dashboard ,
                        category_list,category_delete,category_create,category_update,
                        category_section_view, chat_with_gpt,workout_view
                        )

urlpatterns = [

    path('list_users/', views.list_users, name='list_users'), 

    # path('manage_permissions/', manage_permissions, name='manage_permissions'),

    path('get_user_permissions/<int:user_id>/', get_user_permissions, name='get_user_permissions'),

    path('categories/', category_list, name='categories'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/update/<int:pk>/', category_update, name='category_update'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),

    
    path('category-section/', category_section_view, name='category_section'),

    path('get_permissions/<int:user_id>/', views.get_user_permissions, name='get_user_permissions'),
    path('users/create/', user_create, name='user_create'),
    path('users/update/<int:pk>/', user_update, name='user_update'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),


    path('roles/', role_list, name='role_list'),
    path('roles/create/', role_create, name='role_create'),
    path('roles/update/<int:pk>/', role_update, name='role_update'),
    path('roles/delete/<int:pk>/', role_delete, name='role_delete'),

  
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),


    path('', dashboard, name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),


    path('chat/', chat_with_gpt, name='chat_with_gpt'),
    path('workout/', workout_view, name='workout_view'),
]