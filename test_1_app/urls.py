from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.welcome),
    path('login', views.login),
    path('logout', views.logout),
    path('trip/add', views.add_trip),
    path('trip/create', views.create_trip),
    path('trip/remove/<int:id>', views.remove_trip),
    path('trip/delete/<int:id>', views.delete_trip),
    path('trip/join/<int:id>', views.join_trip),
    path('trip/<int:id>', views.view_trip)
]