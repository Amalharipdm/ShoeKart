from django.contrib import admin
from . models import *

# Register your models here.


class GenderAdmin(admin.ModelAdmin):
    list_display = ('gender_name',)

class ProductCategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'is_blocked')
    actions = ['block_category', 'unblock_category']

    def block_category(self, request, queryset):
        queryset.update(is_blocked=True)

    def block_category(self, request, queryset):
        queryset.update(is_blocked=False)

class ProductBrandsAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'is_blocked')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_brand', 'product_category', 'product_price', 'product_gender', 'product_thumbnail', 'product_description')

class ProductColorsAdmin(admin.ModelAdmin):
    list_display = ('color_name',)


class ProductSizesAdmin(admin.ModelAdmin):
    list_display = ('size_number',)

class ProductImagesAdmin(admin.ModelAdmin):
     list_display = ('name', 'colors')

class ProductVarientAdmin(admin.ModelAdmin):
     list_display = ('name', 'colors', 'size', 'stock')

admin.site.register(Gender, GenderAdmin)
admin.site.register(ProductBrands, ProductBrandsAdmin)
admin.site.register(ProductCategories, ProductCategoriesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColors, ProductColorsAdmin)
admin.site.register(ProductSizes, ProductSizesAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(ProductVarient, ProductVarientAdmin)
