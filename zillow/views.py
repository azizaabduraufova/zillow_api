from django.shortcuts import render
from rest_framework import generics, filters

from zillow.models import PropertyType, Property, Profile
from zillow.permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly
from zillow.serializers import PropertyTypeSerializer, PropertySerializer, UserProfileSerializer
from rest_framework import generics, filters


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
    permission_classes = [IsOwnerOrReadOnly]
