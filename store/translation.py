from .models import Product, Category, SubCategory, Review
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'descriptions')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)