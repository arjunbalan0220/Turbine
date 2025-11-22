from django.urls import path
from .import views
from .views import spare, create_order, cod_payment


urlpatterns=[
    path('',views.index,name='Home'),
    
    
    path('bike/',views.bike,name='bike'),
    path('car/',views.car,name='car'),
    path('company_sep/',views.company_sep,name='company_sep'),
    path('logiin/',views.log,name='log'),
    
    path('company_login/',views.company_login,name='company_login'),
    path('company_home/',views.company_home,name='company_home'),
    path('logout/', views.company_logout, name="company_logout"),
    path('company_add/', views.company_add, name="company_add"),
    path('company_spare/<str:vehicle_id>/', views.company_spare, name="company_spare"),
    path('add_stock/<str:spare_id>/', views.add_stock, name='add_stock'),

    
    
    path('individual_spare/<str:vehicle_id>/', views.individual_spare, name="individual_spare"),
    path('spareview/',views.spareview,name='spareview'),
    path('spare/',views.spare,name='spare'),
    path('delete_spare/<str:spare_id>/', views.delete_spare, name='delete_spare'),
    

    path('create_order/<str:spare_id>/', views.create_order, name='create_order'),
    
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path("order/cod/<str:spare_id>/", cod_payment, name="cod_payment"),
    path('order_success/', views.order_success, name='order_success'),
    path("rate-product/<int:order_id>/", views.rate_product, name="rate_product"),
    path('reviews/<str:spare_id>/', views.view_reviews, name='view_reviews'),




    path('add_cart1/<str:spare_id>/', views.add_cart1, name='add_cart1'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('cart_viewprofile/', views.cart_viewprofile, name='cart_viewprofile'),
    path('remove_cart_item/<int:cart_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('orders/', views.orders, name='orders'),
    path('create_bulk_order/', views.create_bulk_order, name='create_bulk_order'),
    
    path('payment-success_page/', views.payment_success_page, name='payment_success_page'),
    path('api/payment-success/', views.payment_success_api, name='payment_success_api'),


    
    
]
