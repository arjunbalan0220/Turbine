from django.db import models


# Create your models here.
class Accessories(models.Model):
    acc_id = models.CharField(max_length=6,null=False)
    acc_name = models.CharField(max_length=100)
    acc_type = models.CharField(max_length=100,null=True)
    acc_desc = models.TextField(max_length=1000)
    acc_prize = models.CharField(max_length=100)
    image=models.ImageField(upload_to="img",null=True)
    def __str__(self):
        return self.acc_id
    