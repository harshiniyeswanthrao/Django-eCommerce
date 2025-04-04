from django.urls import path
from first_app import views
from django.conf import settings
from django.conf.urls.static import static

# from .views import increase_quantity, decrease_quantity


urlpatterns = [
    path('', views.home_or_shop, name='home_or_shop'),
    path('products/', views.product_list, name='product_list'),
    path('checklist/', views.checklist, name='checklist'),
    path('contact/', views.contact, name='contact'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('shipping-details/', views.shipping_details, name='shipping_details'),
    path('place-order/', views.place_order, name='place_order'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('Orders/', views.my_orders, name='My_Orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
