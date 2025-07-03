from django.urls import path
from toy_factory import views
urlpatterns = [
    path('create_toy/', views.create_toy, name='create_toy'),
    path('view_toys/', views.view_toys, name='view_toys'),
    path('toy/<int:toy_id>/', views.view_toy, name='view_toy'),
    path('assign/', views.assign, name='assign'),
]