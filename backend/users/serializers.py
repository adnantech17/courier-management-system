from rest_framework import serializers
from routing.serializers import BranchSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name',
                  'assigned_branch', 'role', 'password', 'branch']

    # def validate(self, attr):
    #     validate_password(attr['password'])
    #     return attr

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            assigned_branch=validated_data['assigned_branch'],
            email=validated_data['email'],
            name=validated_data['name'],
            role=validated_data['role'],

        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def get_branch(self, obj):
        return BranchSerializer(obj.assigned_branch).data
