from django.urls import path
from django.conf import settings
from myApp import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('pcbuild', views.pcbuild, name='pcbuild'),
    path('products/',views.product_list,name='products'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('signup/',views.register,name='signup'),
    path('categories/',views.category_list,name='categories'),
    path('products/<int:category_id>/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('select_item/<int:product_id>/', views.select_item, name='select_item'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
]

