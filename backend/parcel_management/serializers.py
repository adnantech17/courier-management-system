from rest_framework import serializers

from .models import Parcel, Customer, Address, PathHistory
from routing.serializers import BranchSerializer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class PathHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PathHistory
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

    source_branch = serializers.SerializerMethodField(read_only=True)
    destination_branch = serializers.SerializerMethodField(read_only=True)

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
        print(instance)
        instance.current_tracking_status = validated_data.get(
            'current_tracking_status', instance.current_tracking_status)
        instance.current_branch = validated_data.get(
            'current_branch', instance.current_branch)
        if validated_data.get('parcel_on_return'):
            temp = instance.destination_address
            print(temp)
            instance.destination_address = instance.source_address
            instance.source_address = temp
            print(instance)
        instance.parcel_on_return = validated_data.get(
            'parcel_on_return', instance.parcel_on_return)
        instance.save()

        return instance

    class Meta:
        model = Parcel
        fields = '__all__'
        read_only_fields = ['id']

    def get_source_branch(self, obj):
        return BranchSerializer(obj.source_address.branch).data

    def get_destination_branch(self, obj):
        return BranchSerializer(obj.destination_address.branch).data


class TrackSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = PathHistory
        fields = '__all__'
