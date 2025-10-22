from rest_framework import serializers
from .models import (UserProFile, Category, SubCategory, Product,
                     ProductImage, Review, Cart, CartItem, Favorite, FavoriteItem, )
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProFile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProFile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProFile
        fields =['first_name','last_name']

class UserProFileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProFile
        fields = ['first_name','last_name']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_image','category_name']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name' ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    image_product = ProductImageSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    count_person = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','image_product','price','subcategory','product_name', 'get_avg_rating','count_person']

    def get_avg_rating(self,obj):
        return obj.get_avg_rating()

    def count_person(self,obj):
        return obj.get_count_person()


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_product = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'subcategory_product']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProFileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['id','comment','stars','user','created_date']


class ProductDetailSerializer(serializers.ModelSerializer):
    image_product = ProductImageSerializer(many=True, read_only=True)
    subcategory = SubCategoryListSerializer()
    review_product = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['image_product','price','subcategory','product_name',
                  'article_number','descriptions','video','review_product']




class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['category_name','subcategory']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True,
                                                    source='product')
    class Meta:
        model = CartItem
        fields = ['id', 'product','product_id','quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(read_only=True,
                                                    source='product')
    class Meta:
        model = FavoriteItem
        fields = ['id', 'product','product_id']



class FavoriteSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user']







