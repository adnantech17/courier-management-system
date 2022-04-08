from rest_framework import serializers

from .models import Parcel, Customer, Address


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ParcelSerializer(serializers.ModelSerializer):
    sender = CustomerSerializer(read_only=False)
    receiver = CustomerSerializer(read_only=False)
    source_address = AddressSerializer(read_only=False)
    destination_address = AddressSerializer(read_only=False)

    def create(self, validated_data):
        sender_data = validated_data.pop('sender')
        receiver_data = validated_data.pop('receiver')
        source_address_data = validated_data.pop('source_address')
        destination_address_data = validated_data.pop('destination_address')

        sender = Customer.objects.create(**sender_data)
        receiver = Customer.objects.create(**receiver_data)
        source_address = Address.objects.create(**source_address_data)
        destination_address = Address.objects.create(
            **destination_address_data)

        parcel = Parcel.objects.create(sender=sender, receiver=receiver, source_address=source_address,
                                       destination_address=destination_address, ** validated_data)
        return parcel

    def update(self, instance, validated_data):
        instance.current_tracking_status = validated_data.get(
            'current_tracking_status', instance.current_tracking_status)
        instance.parcel_on_return = validated_data.get(
            'parcel_on_return', instance.parcel_on_return)
        instance.save()

        return instance

    class Meta:
        model = Parcel
        fields = '__all__'
        read_only_fields = ['id']
