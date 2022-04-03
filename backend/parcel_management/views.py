import time
from django.shortcuts import render
from rest_framework.response import Response
from .models import Parcel, Customer, Address
from .serializers import ParcelSerializer, AddressSerializer, CustomerSerializer
from rest_framework import status
from rest_framework.views import APIView


class ParcelAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = Parcel.objects.get(id=id)
            serializer = ParcelSerializer(stu)
            return Response(serializer.data)

        stu = Parcel.objects.all()
        serializer = ParcelSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        sender = request.data["sender"]
        receiver = request.data["receiver"]
        source_address = request.data["source_address"]
        destination_address = request.data["destination_address"]

        serializer = AddressSerializer(data=source_address)
        if serializer.is_valid():
            request.data["source_address"] = serializer.save().id
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddressSerializer(data=destination_address)
        if serializer.is_valid():
            request.data["destination_address"] = serializer.save().id
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=sender)
        if serializer.is_valid():
            request.data["sender"] = serializer.save().id
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=receiver)
        if serializer.is_valid():
            request.data["receiver"] = serializer.save().id
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request.data['tracking_id'] = int(round(time.time() * 1000))

        print(request.data)
        serializer = ParcelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = Parcel.objects.get(pk=id)
        serializer = ParcelSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        stu = Parcel.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'})
