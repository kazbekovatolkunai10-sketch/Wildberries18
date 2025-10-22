from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, generics,status, permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserProFileSerializer, CategoryListSerializer, CategoryDetailSerializer,
                          SubCategoryListSerializer,
                          SubCategoryDetailSerializer, ProductListSerializer, ProductImageSerializer, ReviewSerializer,
                          CartSerializer, CartItemSerializer, ProductDetailSerializer, UserSerializer, LoginSerializer,
                          FavoriteSerializer, FavoriteItemSerializer, )
from .models import (UserProFile, Category, SubCategory, Product, ProductImage, Review, Cart, CartItem, Favorite)
from .filter import ProductFilter
from .pagination import ProductSetPagination
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProFileViewSet(viewsets.ModelViewSet):
    queryset = UserProFile.objects.all()
    serializer_class = UserProFileSerializer

    def get_queryset(self):
        return UserProFile.objects.filter(id=self.request.user.id)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer


class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price']
    pagination_class = ProductSetPagination
    permission_classes = [permissions.IsAuthenticated]


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CartViewSet(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, creates = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)



class FavoriteViewSet(generics.RetrieveAPIView):
    serializer_class = FavoriteSerializer()

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)

class FavoriteItemViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteItemSerializer

    def get_queryset(self):
        return Favorite.objects.filter(favorite__user=self.request.user)

    def perform_create(self, serializer):
        favorite, creates = Favorite.objects.get_or_create(user=self.request.user)
        serializer.save(favorite=favorite)








