from django.db import models
from django.core.validators import MinValueValidator

class Branch(models.Model):
    name = models.CharField(unique=True, max_length=64)
    estimated_processing_time = models.FloatField(validators=[MinValueValidator(0.0)])
    estimated_processing_cost = models.FloatField(validators=[MinValueValidator(0.0)])

    REQUIRED_FIELDS = ['name', 'estimated_processing_time',
                       'estimated_processing_cost']

    def __str__(self):
        return self.name


class BranchEdge(models.Model):
    from_branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='from_branch')
    to_branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='to_branch')
    shipping_time = models.FloatField(validators=[MinValueValidator(0.0)])
    shipping_cost = models.FloatField(validators=[MinValueValidator(0.0)])

    REQUIRED_FIELDS = ['from_branch', 'to_branch',
                       'shipping_time', 'shipping_cost']

    def __str__(self):
        return f'{self.from_branch} to {self.to_branch}'
