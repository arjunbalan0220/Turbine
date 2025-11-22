from django.urls import path
from .import views
urlpatterns=[
    path('',views.index,name='Home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    
    #accessories
    path('accessories/',views.accessories,name='accessories'),
    path('acc_jacket/',views.acc_jacket,name='acc_jacket'),
    path('acc_gloves/',views.acc_gloves,name='acc_gloves'),
    path('acc_pant/',views.acc_pant,name='acc_pant'),
    path('acc_boot/',views.acc_boot,name='acc_boot'),
    path('acc_helmet/',views.acc_helmet,name='acc_helmet'),
    path('acc_lock/',views.acc_lock,name='acc_lock'),
    path('acc_lag/',views.acc_lag,name='acc_lag'),
    path('acc_knee/',views.acc_knee,name='acc_knee'),
    path('accessoryview/',views.accessoryview,name='accessoryview'),
    
]