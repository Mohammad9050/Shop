from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username_id = models.CharField(max_length=50, unique=True)
    balance = models.IntegerField(default=0, auto_created=True)


    def spend(self, n):
        if n > self.balance:
            return False
        else:
            return True


class Cart(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.OneToOneField('Store.Product', on_delete=models.CASCADE)


class PayHistory(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
