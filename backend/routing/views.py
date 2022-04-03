from django.shortcuts import render
from rest_framework.response import Response
from .models import Branch, BranchEdge
from .serializers import BranchSerializer, BranchEdgeSerializer
from rest_framework import status
from rest_framework.views import APIView


class BranchAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = Branch.objects.get(id=id)
            serializer = BranchSerializer(stu)
            return Response(serializer.data)

        stu = Branch.objects.all()
        serializer = BranchSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = Branch.objects.get(pk=id)
        serializer = BranchSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        stu = Branch.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'})


class BranchEdgeAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = BranchEdge.objects.get(id=id)
            serializer = BranchEdgeSerializer(stu)
            return Response(serializer.data)

        stu = BranchEdge.objects.all()
        serializer = BranchEdgeSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BranchEdgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = BranchEdge.objects.get(pk=id)
        serializer = BranchEdgeSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        stu = BranchEdge.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'})
