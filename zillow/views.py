from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from zillow.models import PropertyType, Property, Profile, WatchedHistory
from zillow.serializers import PropertyTypeSerializer, PropertySerializer, UserProfileSerializer, \
    WatchedHistorySerializer
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
    ordering_fields=['created_at','price']
    ordering=['-created_at']





class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class UserProfileGet(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer



class WatchedHistoryView(APIView):
    def get(selfself,request):
        histories=WatchedHistory.objects.all()
        serializer=WatchedHistorySerializer(histories,many=True)
        return Response(serializer.data)