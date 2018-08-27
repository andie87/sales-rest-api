from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from . import serializers
from sales_api.models import Sales, AGGREGATE_CHOICE

import pendulum

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

        return Response({'message':'info', 'an_apiview':an_apiview})

    def post(self, request):
        """return active user with 3 criteria : start date, end date and aggregate level"""

        serializer = serializers.FilterSerializer(data=request.data)

        if serializer.is_valid():
            start_date = pendulum.parse(serializer.data.get('start_date'))
            end_date = pendulum.parse(serializer.data.get('end_date'))
            aggregate = serializer.data.get('agg_level')
            result = []
            info = {}
            info['start_date'] = str(start_date)
            info['end_date'] = str(end_date)
            info['agg_level'] = aggregate
            data = []
            period = pendulum.period(start_date, end_date)
            if aggregate == AGGREGATE_CHOICE[0]: #if aggregate is daily                
                period = pendulum.period(start_date, end_date)
                for dt in period.range('days'):
                    day = {}
                    temp_daily =  Sales.objects.filter(purchased_date__day=dt.strftime('%d'),purchased_date__month=dt.strftime('%m'),purchased_date__year=dt.strftime('%Y')).order_by('-purchased_date')
                    sales_serializer = serializers.SalesSerializer(temp_daily, many=True)
                    day['date'] = str(dt)
                    day['data'] = sales_serializer.data
                    data.append(day)
            elif aggregate == AGGREGATE_CHOICE[1]: #if aggregate is weekly
                if start_date.day_of_week == pendulum.MONDAY:
                    temp_start_date = start_date
                else:
                    temp_start_date = start_date.start_of('week')
                period = pendulum.period(temp_start_date, end_date)
                i = 0
                for dt in period.range('weeks'):
                    week = {}
                    if i == 0:
                        temp_weekly =  Sales.objects.filter(purchased_date__gt=start_date.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('week')).order_by('-purchased_date')
                        sales_serializer = serializers.SalesSerializer(temp_weekly, many=True)
                        week['period'] = str(start_date.start_of('day'))+" to "+str(dt.end_of('week'))
                        week['data'] = sales_serializer.data
                    else :
                        temp_weekly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('week')).order_by('-purchased_date')
                        sales_serializer = serializers.SalesSerializer(temp_weekly, many=True)
                        week['period'] = str(dt.start_of('day'))+" to "+str(dt.end_of('week'))
                        week['data'] = sales_serializer.data
                    data.append(week)
                    i+=1
            else:
                if start_date.format('DD') == '01':
                    temp_start_date = start_date
                else:
                    temp_start_date = start_date.start_of('month')
                period = pendulum.period(temp_start_date, end_date)
                i = 0
                for dt in period.range('months'):
                    month = {}
                    if i == 0:
                        temp_monthly =  Sales.objects.filter(purchased_date__gt=start_date.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('month')).order_by('-purchased_date')
                        sales_serializer = serializers.SalesSerializer(temp_monthly, many=True)
                        month['period'] = str(start_date.start_of('day'))+" to "+str(dt.end_of('month'))
                        month['data'] = sales_serializer.data
                    else :
                        temp_monthly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('month')).order_by('-purchased_date')
                        sales_serializer = serializers.SalesSerializer(temp_monthly, many=True)
                        month['period'] = str(dt.start_of('day'))+" to "+str(dt.end_of('month'))
                        month['data'] = sales_serializer.data
                    data.append(month)
                    i+=1

            result.append({'info':info, 'result':data})            
            return Response(result)
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

        return Response({'message':'info', 'an_apiview':an_apiview})

    def post(self, request):
        """return total revenue with 3 criteria : start date, end date and aggregate level"""

        serializer = serializers.FilterSerializer(data=request.data)
        #return Response({"pesan":"halooo"})

        if serializer.is_valid():
            start_date = pendulum.parse(serializer.data.get('start_date'))
            end_date = pendulum.parse(serializer.data.get('end_date'))
            aggregate = serializer.data.get('agg_level')
            result = []
            if aggregate == AGGREGATE_CHOICE[0]: #if aggregate is daily
                period = pendulum.period(start_date, end_date)
                day = {}
                for dt in period.range('days'):
                    temp_daily =  Sales.objects.filter(purchased_date__day=dt.strftime('%d'),purchased_date__month=dt.strftime('%m'),purchased_date__year=dt.strftime('%Y')).order_by('-purchased_date')
                    total = temp_daily.aggregate(Sum('amount'))
                    day[str(dt)] = total
                result.append(day)    
            elif aggregate == AGGREGATE_CHOICE[1]: #if aggregate is weekly
                result = Sales.objects.filter(purchased_date__range=[start_date,end_date]).order_by('-purchased_date')
            else:
                result = Sales.objects.filter(purchased_date__range=[start_date,end_date]).order_by('-purchased_date')
                        
            return Response(result)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)