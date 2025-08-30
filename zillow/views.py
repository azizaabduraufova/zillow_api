
from django.shortcuts import render
from rest_framework import generics, filters
from django.contrib.auth import authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from zillow.models import PropertyType, Property, Profile
from zillow.serializers import PropertyTypeSerializer,PropertySerializer, UserProfileSerializer, LoginUserSerializer
from typing import reveal_type

from django.core.serializers import serialize
from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework import generics, filters
from django.contrib.auth.models import User   # ✅ To‘g‘ri
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from zillow.models import PropertyType, Property, Profile, WatchedHistory
from zillow.permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly
from zillow.serializers import (
    PropertyTypeSerializer,
    PropertySerializer,
    UserProfileSerializer,
    WatchedHistorySerializer, PropertyStatisticsSerializer,
)


class PropertyTypeGet(generics.ListCreateAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']


class PropertyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class PropertyGet(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']
    permission_classes = [IsSellerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(listed_by=self.request.user)


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsSellerOrReadOnly]


class UserProfileGet(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

class RegisterUserProfile(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response({
            "message": "User successfully created",
            "user": serializer.data,
            "token": str(token.key)
        }, status=status.HTTP_201_CREATED)


class LoginUserAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "User logged out!"})
    permission_classes = [IsOwnerOrReadOnly]


# class WatchedHistoryView(APIView):
#     def get(selfself,request):
#         histories=WatchedHistory.objects.all()
#         serializer=WatchedHistorySerializer(histories,many=True)
#         return Response(serializer.data)
#     def post(selfself,request):
#         serializer=WatchedHistorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=HTTP_201_CREATED)


class WatchedHistoryView(APIView):
    def get(self,  request):
        histories=WatchedHistory.objects.filter(is_deleted=False)
        serializer=WatchedHistorySerializer(histories,many=True)
        films=WatchedHistory.objects.aggregate(
            watched_films_count=Count('id',filter=Q(is_deleted=False)),
            history_clear=Count('id',filter=Q(is_deleted=True))
        )
        return Response({
            "watched_films_count":films["watched_films_count"],
            "history_clear":films["history_clear"],
            "histories":serializer.data
        })


class WatchedHistoryDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchedHistory.objects.filter(is_deleted=True)
    serializer_class = WatchedHistorySerializer


class PropertyStatisticsView(APIView):
    def get (self,request):
        property=Property.objects.annotate(watched_properties_count=Count('watched_history'))
        serializer=PropertyStatisticsSerializer(property,many=True)
        return Response(serializer.data)
