from rest_framework import serializers

from .models import Branch, BranchEdge


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['id', 'name', 'estimated_processing_time',
                  'estimated_processing_cost']


class BranchEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchEdge
        fields = ['id', 'from_branch', 'to_branch',
                  'shipping_time', 'shipping_cost']
