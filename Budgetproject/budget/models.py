from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=120)
    address=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=12)
    username=models.CharField(max_length=120)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    category_name=models.CharField(max_length=200)


    def __str__(self):
        return self.category_name


class Budget(models.Model):
    user=models.CharField(max_length=120)
    category_type=models.ForeignKey(Category,on_delete=models.CASCADE)
    expenses=models.IntegerField()
    date= models.DateField()
    description=models.TextField(blank=True)

    def __str__(self):
        return str(self.user)