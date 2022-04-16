import time
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.response import Response
from parcel_management.graph import Graph

from routing.models import Branch, BranchEdge
from routing.serializers import BranchSerializer
from .models import Address, Parcel, PathHistory
from .serializers import ParcelSerializer,  PathHistorySerializer, TrackSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class CheckReceiveAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        try:
            data = Parcel.objects.get(id=pk)
        except:
            return Response({'data': {'msg': 'Parcel not found'}, 'success': False}, status=status.HTTP_404_NOT_FOUND)
        else:
            if request.user.role != 'office_staff' or data.current_tracking_status != 'shipping':
                return Response({'data': {'msg': 'Invalid parcel entry'}, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ParcelSerializer(data)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        arr = request.data['serials'].split(',')
        
        if request.user.role != 'office_staff':
            return Response({'data': {'msg': "You don't have the permission"}, 'success': False})

        for id in arr:
            try:
                parcel = Parcel.objects.get(id=int(id))
                branch = request.user.assigned_branch

                new_status = 'arrived' if branch == parcel.destination_address.branch else 'processing'

                serializer = ParcelSerializer(
                    parcel, data={'current_tracking_status': new_status, 'current_branch': request.user.assigned_branch.id}, partial=True)
                if serializer.is_valid():
                    serializer.save()

                serializer = PathHistorySerializer(
                    data={'parcel': parcel.id, 'branch': branch.id})
                if serializer.is_valid():
                    serializer.save()

            except Exception as e:
                return Response({'data': 'Invalid Input', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)


class CheckRouteAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        try:
            data = Parcel.objects.get(id=pk)
        except:
            return Response({'data': {'msg': 'Parcel not found'}, 'success': False}, status=status.HTTP_404_NOT_FOUND)
        else:
            print(data.current_branch, request.user.assigned_branch)
            if request.user.role != 'office_staff' or data.current_tracking_status == 'shipping' or (data.current_branch == request.user.assigned_branch and data.current_branch == data.destination_address.branch) or data.current_branch != request.user.assigned_branch:
                return Response({'data': {'msg': 'Invalid parcel entry'}, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ParcelSerializer(data)

        all_data = BranchEdge.objects.all()
        graph = Graph(all_data, request.user.assigned_branch.id,
                      data.destination_address.branch.id)
        path, _ = graph.shortest_path()

        path.popleft()

        newDict = {}

        if len(path):
            next_branch = Branch.objects.get(id=path.popleft())
            next_serializer = BranchSerializer(next_branch)
            newDict = {'next_route': next_serializer.data}

        newDict.update(serializer.data)

        return Response({'data': newDict, 'success': True})

    def post(self, request, format=None):
        arr = request.data['serials'].split(',')
        
        if request.user.role != 'office_staff':
            return Response({'data': {'msg': "You don't have the permission"}, 'success': False})

        for id in arr:
            try:
                parcel = Parcel.objects.get(id=int(id))

                serializer = ParcelSerializer(
                    parcel, data={'current_tracking_status': 'shipping'}, partial=True)
                if serializer.is_valid():
                    serializer.save()

            except:
                return Response({'data': {'msg': 'Failed to route'}, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)


class ParcelAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            data = Parcel.objects.get(id=id)
            serializer = ParcelSerializer(data)
            return Response(serializer.data)

        all_data = Parcel.objects.all()
        total = all_data.count()

        if request.user.role == 'delivery_man':
            print(request.user.assigned_branch.id)
            all_data = Parcel.objects.filter(
                current_tracking_status='arrived', destination_address__branch__id=request.user.assigned_branch.id)
            total = all_data.count()

        if request.user.role == 'office_staff':
            print(request.user.assigned_branch.id)
            all_data = Parcel.objects.filter(
                current_branch__id=request.user.assigned_branch.id)
            total = all_data.count()

        pageSize = request.query_params.get("pageSize")
        page = request.query_params.get('current')

        if pageSize is None:
            pageSize = 10

        if page is None:
            page = 1

        paginator = Paginator(all_data, pageSize)
        dataResponse = int(pageSize) > 0 and paginator.page(page) or all_data
        serializer = ParcelSerializer(dataResponse, many=True)

        return Response({'data': serializer.data, 'success': True, 'page': page, 'pageSize': pageSize, 'total': total})

    def post(self, request, format=None):

        request.data['tracking_id'] = int(round(time.time() * 1000))
        request.data['current_branch'] = request.data['source_address']['branch']

        all_data = BranchEdge.objects.all()
        graph = Graph(all_data,
                      request.data['source_address']['branch'], request.data['destination_address']['branch'])
        _, cost = graph.shortest_path()

        serializer = ParcelSerializer(data=request.data)
        if serializer.is_valid():
            if cost == -1:
                return Response({'data': {'msg': 'Unable to find any path between source and destination'}, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response({'data': {'msg': 'Data Created', 'tracking_id': request.data['tracking_id'], 'cost': cost}, 'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Parcel.objects.get(pk=id)
        new_data = {}
        new_data['current_tracking_status'] = request.data.get(
            'current_tracking_status')

        if request.data.get('parcel_on_return') == True or request.data.get('current_tracking_status') == 'delivered':
            if request.user.assigned_branch == data.destination_address.branch and request.user.role == 'delivery_man':
                new_data['parcel_on_return'] = request.data['parcel_on_return']
            else:
                return Response({'data': {'msg': "You don't have the permission"}, 'success': False})

        serializer = ParcelSerializer(data, data=new_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Partial Data Updated'}, 'success': True})
        return Response({'data': serializer.errors, 'success': False})

    def delete(self, request, pk, format=None):
        id = pk
        data = Parcel.objects.get(pk=id)
        data.delete()
        return Response({'msg': 'Data Deleted'})


class TrackAPI(APIView):
    def get(self, request, format=None):
        id = request.query_params.get("id")
        phone = request.query_params.get("phone")
        if phone:
            all_parcels = Parcel.objects.filter(sender__contact_number=phone)
            if(all_parcels.count() == 0):
                return Response({'data': {'msg': "No Parcel Found"}, 'type': 'parcels', 'success': False}, status=status.HTTP_404_NOT_FOUND)

            serializer = ParcelSerializer(all_parcels, many=True)
            return Response({'data': serializer.data, 'type': 'parcels', 'success': True})

            # id = Parcel.objects.get(sender__contact_number=phone).id
        all_data = PathHistory.objects.filter(parcel=id)
        if(all_data.count() == 0):
            return Response({'data': {'msg': "No Parcel Found"}, 'type': 'tracks', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = TrackSerializer(all_data, many=True)
        return Response({'data': serializer.data, 'type': 'tracks', 'success': True})
