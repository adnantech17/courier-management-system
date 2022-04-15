from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class CurrentUserAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'data': serializer.data, 'success': True})


class UsersAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Updated'}, 'success': True})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        user.delete()
        return Response({'msg': 'Data Deleted'})
