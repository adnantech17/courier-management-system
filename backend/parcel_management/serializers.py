from rest_framework import serializers

from .models import Parcel, Customer, Address


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'contact_number']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'detailed_address', 'branch']


class ParcelSerializer(serializers.ModelSerializer):
    sender = CustomerSerializer(read_only=False)
    receiver = CustomerSerializer(read_only=False)
    source_address = AddressSerializer(read_only=False)
    destination_address = AddressSerializer(read_only=False)

    def create(self, validated_data):
        parcel = Parcel.objects.create(**validated_data)
        return parcel

    class Meta:
        model = Parcel
        fields = ['id', 'name', 'tracking_id',
                  'source_address', 'destination_address', 'sender', 'receiver',
                  'current_tracking_status', 'parcel_on_return']
        read_only_fields = ['id']
