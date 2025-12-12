from django.db import models

class Product(models.Model):
    IdProduct = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    CurrentStock = models.IntegerField()

    def __str__(self):
        return self.Name
