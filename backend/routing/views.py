from os import stat
from django.shortcuts import render
from rest_framework.response import Response

from parcel_management.graph import Graph
from .models import Branch, BranchEdge
from .serializers import BranchSerializer, BranchEdgeSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator


class BranchAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = Branch.objects.get(id=id)
            serializer = BranchSerializer(stu)
            return Response(serializer.data)

        all_data = Branch.objects.all()
        pageSize = request.query_params.get("pageSize")
        page = request.query_params.get('page')

        if pageSize is None:
            pageSize = 10

        if page is None:
            page = 1

        paginator = Paginator(all_data, pageSize)
        dataResponse = int(pageSize) > 0 and paginator.page(page) or all_data
        serializer = BranchSerializer(dataResponse, many=True)
        return Response({'data': serializer.data, 'success': True, 'page': page, 'pageSize': pageSize}, status = status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = Branch.objects.get(pk=id)
        serializer = BranchSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Updated'}, 'success': True}, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        id = pk
        stu = Branch.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'}, status = status.HTTP_200_OK)


class BranchEdgeAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = BranchEdge.objects.get(id=id)
            serializer = BranchEdgeSerializer(stu)
            return Response(serializer.data,status=status.HTTP_200_OK)

        all_data = BranchEdge.objects.all()
        pageSize = request.query_params.get("pageSize")
        page = request.query_params.get('page')

        if pageSize is None:
            pageSize = 10

        if page is None:
            page = 1

        paginator = Paginator(all_data, pageSize)
        dataResponse = int(pageSize) > 0 and paginator.page(page) or all_data
        serializer = BranchEdgeSerializer(dataResponse, many=True)
        return Response({'data': serializer.data, 'success': True, 'page': page, 'pageSize': pageSize}, status = status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BranchEdgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = BranchEdge.objects.get(pk=id)
        serializer = BranchEdgeSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Updated'}, 'success': True}, status=status.HTTP_202_ACCEPTED),
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        id = pk
        stu = BranchEdge.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'}, status=status.HTTP_200_OK)
