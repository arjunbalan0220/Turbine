from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='Home'),
    path('login/',views.signin,name='signin'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('logout/', views.user_logout, name="user_logout"),
]