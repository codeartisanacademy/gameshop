from django.db import models
from model_utils.models import TimeStampedModel

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

    def get_discounted_price(self, discount):
        return self.price - (self.price * (discount/100))


class ProductImage(TimeStampedModel):
    pass
    