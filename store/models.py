from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProFile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators = [MinValueValidator(15),
                                           MaxValueValidator(70)],null=True,blank=True)
    phone_number = PhoneNumberField()
    STATUS_CHOICES = (
        ('gold','gold'),#75
        ('silver','silver'),#50
        ('bronze','bronze'),#25
        ('simple','simple'),#0
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='simple')
    data_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    category_image = models.ImageField(upload_to='category_image/')
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name = 'sub_category')
    subcategory_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory_product')
    article_number = models.PositiveSmallIntegerField(unique=True)
    descriptions = models.TextField()
    video = models.FileField(upload_to='video/',null=True,blank=True)

    def __str__(self):
        return f'{self.product_name},{self.price},{self.subcategory},{self.article_number},{self.descriptions},{self.video}'

    def get_avg_rating(self):
        rating = self.review_product.all()
        if rating.exists():
            return round(sum([i.stars for i in rating]) / rating.count(),1)
        return 0


    def count_person(self):
        rating = self.review_product.all()
        return rating.count()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_product')
    image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return f'{self.product.product_name}'


class Review(models.Model):
    user = models.ForeignKey(UserProFile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name ='review_product')
    comment = models.TextField(null=True,blank=True)
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,6)],null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class Cart(models.Model):
    user = models.OneToOneField(UserProFile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.cart}, {self.product}, {self.quantity}'


class Favorite(models.Model):
    user = models.OneToOneField(UserProFile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.favorite}, {self.product}'

