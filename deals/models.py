from django.db import models


class Deals(models.Model):
    customer = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(max_length=30)
    auto_increment_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.customer
