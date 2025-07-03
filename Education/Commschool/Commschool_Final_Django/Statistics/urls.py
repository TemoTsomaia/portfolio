from django.urls import path
from Statistics import views

urlpatterns = [
    path('count_lists/', views.count_lists, name='count_lists'),
    path('demand/', views.count_demand, name='count_demand'),
    path('sum_TTC/', views.sum_times_to_create, name='sum_times'),
    path('sum_TTD/', views.sum_times_to_deliver, name='sum_times_to_deliver'),
]