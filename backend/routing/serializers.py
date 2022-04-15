from rest_framework import serializers

from .models import Branch, BranchEdge


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['id', 'name', 'estimated_processing_time',
                  'estimated_processing_cost']


class BranchEdgeSerializer(serializers.ModelSerializer):
    from_branch_name = serializers.SerializerMethodField(read_only=True)
    to_branch_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BranchEdge
        fields = ['id', 'from_branch', 'to_branch',
                  'shipping_time', 'shipping_cost', 'from_branch_name', 'to_branch_name']

    def get_from_branch_name(self, obj):
        return {'name': obj.from_branch.name}

    def get_to_branch_name(self, obj):
        return {'name': obj.to_branch.name}
