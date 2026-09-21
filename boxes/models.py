from django.db import models


class Box(models.Model):
    name = models.CharField(max_length=200)

    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)

    max_weight = models.DecimalField(max_digits=10,decimal_places=2)

    cost = models.DecimalField( max_digits=10,decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name