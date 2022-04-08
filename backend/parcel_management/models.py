from django.db import models
from routing.models import Branch


class Customer(models.Model):
    name = models.CharField(max_length=64)
    contact_number = models.CharField(max_length=64)


class Address(models.Model):
    detailed_address = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Parcel(models.Model):
    name = models.CharField(max_length=64)
    tracking_id = models.IntegerField()
    source_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='source_address')
    destination_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name='destination_address')
    sender = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='receiver')
    current_tracking_status = models.CharField(max_length=64)
    parcel_on_return = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'source_address',
                       'destination_address', 'sender', 'receiver',
                       'current_tracking_status']

    def __str__(self):
        return self.name
