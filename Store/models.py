from django.db import models
from taggit.managers import TaggableManager


class Product(models.Model):
    ANY = 'AN'
    TECHNOLOGY = 'TE'
    FOOD = 'FO'
    CLOTHING = 'Cl'
    OTHER = 'OT'
    CATEGORY = [
        (ANY, 'category(any)'),
        (TECHNOLOGY, 'Technology'),
        (FOOD, 'Food'),
        (CLOTHING, 'Clothing'),
        (OTHER, 'Other'),

    ]
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    inventory = models.IntegerField(default=1)
    category = models.CharField(max_length=2, choices=CATEGORY, default='OT')
    product_img = models.ImageField(upload_to='photos/', default='photos/default_store.jpg')
    tags = TaggableManager()

    def increase(self, num):
        if self.inventory < num:
            return False
        self.inventory -= num
        self.save()
        return True

    def __str__(self):
        return self.name


class Receipt(models.Model):
    customer = models.ForeignKey('Accounts.Profile', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    buy_time = models.DateTimeField(auto_now_add=True)
