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
        print(request.user)
        user = request.user
        serializer = UserSerializer(user)
        return Response({'data': serializer.data, 'success': True})


class UsersAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = User.objects.get(id=id)
            serializer = UserSerializer(stu)
            return Response(serializer.data)

        stu = User.objects.all()
        serializer = UserSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = UserSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        stu = User.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'})
