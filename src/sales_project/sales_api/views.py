from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers

# Create your views here.
class ActiveUserApiView(APIView):
    """Active User API View."""

    serializer_class = serializers.FilterSerializer

    def get(self, request, format=None):
        """Return a list of APIView features."""

        an_apiview = [
            "Uses HTTP methods as function (get, post)",
            "get function return this information",
            "post function is to get active user with 3 criteria : start date, end date and aggregate level"
        ]

        return Response({'message':'hello', 'an_apiview':an_apiview})

    def post(self, request):
        """return active user with 3 criteria : start date, end date and aggregate level"""

        serializer = serializers.FilterSerializer(data=request.data)

        if serializer.is_valid():
            start_date = serializer.data.get('start_date')
            end_date = serializer.data.get('end_date')
            aggregate = serializer.data.get('agg_level')
            return Response({'start_date': start_date, 'end_date': end_date, 'aggregate_level': aggregate})
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TotalRevenueApiView(APIView):
    """Total Revenue API View."""

    serializer_class = serializers.FilterSerializer

    def get(self, request, format=None):
        """Return a list of APIView features."""

        an_apiview = [
            "Uses HTTP methods as function (get, post)",
            "get function return this information",
            "post function is to get total revenue with 3 criteria : start date, end date and aggregate level"
        ]

        return Response({'message':'hello', 'an_apiview':an_apiview})

    def post(self, request):
        """return total revenue with 3 criteria : start date, end date and aggregate level"""

        serializer = serializers.FilterSerializer(data=request.data)

        if serializer.is_valid():
            start_date = serializer.data.get('start_date')
            end_date = serializer.data.get('end_date')
            aggregate = serializer.data.get('agg_level')
            return Response({'start_date': start_date, 'end_date': end_date, 'aggregate_level': aggregate})
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)