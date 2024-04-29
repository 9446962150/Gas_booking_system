from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    User=models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.User.username

class Product(models.Model):
    Gid=models.BigAutoField(primary_key=True)
    price= models.FloatField()
    quantity=models.IntegerField()
    subsidy=models.FloatField()
    def __str__(self):
        return str(self.Gid)

class Orders(models.Model):
    id=models.BigAutoField(primary_key=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    Gid=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    amount= models.FloatField()
    order_status=models.CharField(max_length=50)
    order_date=models.DateField()
    delivery_date=models.DateField(null=True)
    pay_mode=models.CharField(max_length=50)
    pay_status=models.CharField(max_length=50)
    def __str__(self):
        return str(self.id)
    
class Feedback(models.Model):
    id=models.BigAutoField(primary_key=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    def __str__(self):
        return str(self.id)
