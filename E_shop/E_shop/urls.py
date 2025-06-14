"""
URL configuration for E_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store_app import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),#nip pass nip47
    path('',views.HOME,name="home"),   
    path('base.html', views.BASE, name='base'),
    path('product/',views.PRODUCT_view,name='product'),
    path('search/',views.SEARCH,name='search'),
    path('products/<str:id>',views.PRODUCT_DETAILS,name='product_details'),
    path('contact/',views.CONTACT_PAGE,name='contact'),
    path('register/',views.HANDLEREGISTER,name='register'),
    path('login/',views.HANDLELOGIN,name='login'),
    path('logout/',views.HANDLELOGOUT,name='logout'),
    
    
    #cart urls
    path('add/<int:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/',views.cart,name='cart'),
    
    path('checkout/', views.CHECKOUT, name='checkout'),
    path('place_order/', views.PLACE_ORDER, name='place_order'),
    
    path('thankyou/',views.THANKYOU, name='thankyou'),
    path('my_order/', views.MY_ORDERS, name='my_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
