from django.db import models
from django.contrib.auth.models import User

class category(models.Model):
    category_name = models.CharField(max_length=255)

class product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True)
    pname = models.CharField(max_length=255)
    price = models.IntegerField()
    prdt_desc = models.CharField(max_length=255)
    prdt_image = models.ImageField(upload_to="image/",null=True)

class userdetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    prof_image = models.ImageField(upload_to="image/", null=True)

class carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    def total_cost(self):
        return self.quantity * self.product.price
    
class order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    credit_card = models.CharField(max_length=16)
    expire_date = models.DateField()
    cvv = models.CharField(max_length=4)