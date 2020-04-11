from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.urls import reverse

# Create your models here.
class Product(TimeStampedModel):
    CATEGORIES = (
        (1, 'Console'),
        (2, 'Accessories'),
        (3, 'Game Disc'),
    )

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    on_stock = models.PositiveIntegerField()
    category = models.PositiveIntegerField(choices= CATEGORIES)
    
    def __str__(self):
        return self.name
    
    
    @property
    def is_available(self):
        return self.on_stock>0

    @property
    def main_image(self):
        return self.images.first()

    def get_discounted_price(self, discount):
        return self.price - (self.price * (discount/100))
    

class ProductImage(TimeStampedModel):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    