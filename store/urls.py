from django.urls import path, include
from rest_framework import routers
from .views import (UserProFileViewSet, CategoryListAPIView, CategoryDetailAPIView, SubCategoryListAPIView,
                    SubCategoryDetailAPIView,
                    ProductListAPIView, ProductImageViewSet, ProductDetailAPIView, ReviewViewSet,
                    CartViewSet, CartItemViewSet, RegisterView, CustomLoginView, LogoutView, FavoriteViewSet,
                    FavoriteItemViewSet)

router = routers.SimpleRouter()
router.register(r'user', UserProFileViewSet)
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path ('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('category/',CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>/',CategoryDetailAPIView.as_view(), name='category-detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='subcategory-list'),
    path('sub_category/<int:pk>', SubCategoryDetailAPIView.as_view(), name='subcategory-detail'),
    path('product/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='subcategory-detail'),
    path('cart/', CartViewSet.as_view(), name='cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('favorite/', FavoriteViewSet.as_view(), name='favorite'),
    path('favorite_item/<int:pk>/', FavoriteItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

]