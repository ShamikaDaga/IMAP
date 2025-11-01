from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pies/', views.pies_list, name='pies_list'),
    path('cupcakes/', views.cupcakes_list, name='cupcakes_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('payment/', views.payment, name='payment'),
    path('receipt/<int:order_id>/', views.receipt, name='receipt'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
]
