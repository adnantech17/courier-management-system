import time
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.response import Response
from .models import Parcel, Customer, Address
from .serializers import ParcelSerializer, AddressSerializer, CustomerSerializer
from rest_framework import status
from rest_framework.views import APIView


class ParcelAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            all_data = Parcel.objects.get(id=id)
            serializer = ParcelSerializer(all_data)
            return Response(serializer.data)

        all_data = Parcel.objects.all()
        pageSize = request.query_params.get("pageSize")
        page = request.query_params.get('page')

        if pageSize is None:
            pageSize = 10

        if page is None:
            page = 1

        paginator = Paginator(all_data, pageSize)
        dataResponse = int(pageSize) > 0 and paginator.page(page) or all_data
        serializer = ParcelSerializer(dataResponse, many=True)
        return Response({'data': serializer.data, 'success': True, 'page': page, 'pageSize': pageSize})

    def post(self, request, format=None):

        request.data['tracking_id'] = int(round(time.time() * 1000))
        serializer = ParcelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Parcel.objects.get(pk=id)
        serializer = ParcelSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        data = Parcel.objects.get(pk=id)
        data.delete()
        return Response({'msg': 'Data Deleted'})
