from django.db import models
from django.urls import reverse

# Create your models here.

class Gender(models.Model):
    gender_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.gender_name
    

class ProductBrands(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.brand_name
    
    class Meta:
        verbose_name = 'productbrand'
        verbose_name_plural = 'productbrands'

class ProductCategories(models.Model):
    category_name = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name
    
    
    class Meta:
        verbose_name = 'productcategory'
        verbose_name_plural = 'productcategories'


class ProductSizes(models.Model):
    size_number = models.IntegerField()
    
    def __str__(self):
        return str(self.size_number)
    
    class Meta:
        verbose_name = 'productsize'
        verbose_name_plural = 'productsizes'

   # product_images      = models.ImageField(upload_to='images/products')


class ProductColors(models.Model):
    color_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.color_name
    
    class Meta:
        verbose_name = 'productcolor'
        verbose_name_plural = 'productcolors'

    # product_sizes       = models.ManyToManyField(ProductSizes)

class Product(models.Model):
    product_name        = models.CharField(max_length=100, unique=True)
    product_brand       = models.ForeignKey(ProductBrands, on_delete=models.CASCADE)
    product_category    = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    product_price       = models.IntegerField()
    product_gender      = models.ForeignKey(Gender, on_delete=models.CASCADE)
    product_thumbnail      = models.ImageField(upload_to='images/products', default=None, blank=True, null=True)
    product_description = models.TextField(max_length=500, blank=True)


    def __str__(self):
        return self.product_name 
    


class ProductImages(models.Model):
    name            = models.ForeignKey(Product, on_delete=models.CASCADE)
    colors          = models.ForeignKey(ProductColors, on_delete=models.CASCADE, default=None)
    image_1      = models.ImageField(upload_to='images/products', default=None)
    image_2      = models.ImageField(upload_to='images/products', default=None)
    image_3      = models.ImageField(upload_to='images/products', default=None)


    def __str__(self):
        return str(self.colors)
    
class ProductVarient(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    colors = models.ForeignKey(ProductImages, on_delete = models.CASCADE)
    size = models.ForeignKey(ProductSizes, on_delete = models.CASCADE)
    stock = models.IntegerField()
  
    def __str__(self):
        return str(self.stock)


