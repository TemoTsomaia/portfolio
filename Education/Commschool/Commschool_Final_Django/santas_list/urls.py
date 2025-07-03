from django.urls import path
from santas_list import views

urlpatterns = [
    path('create_list/', views.create_list, name='create_list'),
    path('nice_list/', views.view_nice, name='view_nice'),
    path('naughty_list/', views.view_naughty, name='view_naughty'),
    path('all_kids/', views.view_all_kids, name='view_all_kids'),
    path('remove_kid/<int:kid_id>/', views.remove_kid, name='remove_kid'),
    path('kid/<int:kid_id>/', views.view_kid, name='view_kid'),
    path('create_kid/', views.create_kid, name= 'create_kid'),
]