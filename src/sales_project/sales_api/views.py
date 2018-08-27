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
        user_level = self.request.META['HTTP_USER_LEVEL']
        if user_level == 'Admin' or user_level == 'Staff': #both admin and staff can access API
            serializer = serializers.FilterSerializer(data=request.data)

            if serializer.is_valid():
                start_date = pendulum.parse(serializer.data.get('start_date'))
                end_date = pendulum.parse(serializer.data.get('end_date'))
                aggregate = serializer.data.get('agg_level')
                result = []
                request = {}
                request['start_date'] = str(start_date)
                request['end_date'] = str(end_date)
                request['agg_level'] = aggregate
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
                    temp_start_date = start_date.start_of('week')
                    period = pendulum.period(temp_start_date, end_date)
                    i = 0
                    for dt in period.range('weeks'):
                        week = {}
                        if i == 0: #First Week
                            temp_weekly =  Sales.objects.filter(purchased_date__gt=start_date.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('week')).order_by('-purchased_date')
                            week['period'] = str(start_date.start_of('day'))+" to "+str(dt.end_of('week')) 
                        else :
                            if i == period.weeks: #The Last Week
                                temp_weekly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=end_date).order_by('-purchased_date')
                                week['period'] = str(dt.start_of('day'))+" to "+str(end_date)
                            else:
                                temp_weekly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('week')).order_by('-purchased_date')
                                week['period'] = str(dt.start_of('day'))+" to "+str(dt.end_of('week'))
                        
                        sales_serializer = serializers.SalesSerializer(temp_weekly, many=True)
                        week['data'] = sales_serializer.data
                        data.append(week)
                        i+=1
                else: #if aggregate is monthly
                    temp_start_date = start_date.start_of('month')
                    period = pendulum.period(temp_start_date, end_date)
                    i = 0
                    for dt in period.range('months'):
                        month = {}
                        if i == 0:
                            temp_monthly =  Sales.objects.filter(purchased_date__gt=start_date.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('month')).order_by('-purchased_date')
                            month['period'] = str(start_date.start_of('day'))+" to "+str(dt.end_of('month'))
                        else:
                            if i == period.in_months():
                                temp_monthly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=end_date).order_by('-purchased_date')
                                month['period'] = str(dt.start_of('day'))+" to "+str(end_date)
                            else:
                                temp_monthly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('month')).order_by('-purchased_date')
                                month['period'] = str(dt.start_of('day'))+" to "+str(dt.end_of('month'))

                        sales_serializer = serializers.SalesSerializer(temp_monthly, many=True)
                        month['data'] = sales_serializer.data
                        data.append(month)
                        i+=1

                result.append({'request':request, 'result':data})            
                return Response(result)
            else :
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response("You don't have authorization", status=status.HTTP_403_FORBIDDEN)

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
        user_level = self.request.META['HTTP_USER_LEVEL']
        if user_level != 'Admin': #only admin can access API
            return Response("You don't have authorization", status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.FilterSerializer(data=request.data)
        
        if serializer.is_valid():
            start_date = pendulum.parse(serializer.data.get('start_date'))
            end_date = pendulum.parse(serializer.data.get('end_date'))
            aggregate = serializer.data.get('agg_level')
            request = {}
            request['start_date'] = str(start_date)
            request['end_date'] = str(end_date)
            request['agg_level'] = aggregate
            data = []
            result = []
            if aggregate == AGGREGATE_CHOICE[0]: #if aggregate is daily
                period = pendulum.period(start_date, end_date)
                
                for dt in period.range('days'):
                    temp_daily =  Sales.objects.filter(purchased_date__day=dt.strftime('%d'),purchased_date__month=dt.strftime('%m'),purchased_date__year=dt.strftime('%Y')).order_by('-purchased_date')
                    total = temp_daily.aggregate(Sum('amount'))
                    day = {}
                    day['date'] = str(dt)
                    day['total'] = total['amount__sum']
                    data.append(day)
            elif aggregate == AGGREGATE_CHOICE[1]: #if aggregate is weekly
                temp_start_date = start_date.start_of('week')
                period = pendulum.period(temp_start_date, end_date)
                i = 0
                for dt in period.range('weeks'):
                    week = {}
                    if i == 0: #First Week
                        temp_weekly =  Sales.objects.filter(purchased_date__gt=start_date.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('week')).order_by('-purchased_date')
                        week['period'] = str(start_date.start_of('day'))+" to "+str(dt.end_of('week')) 
                    else :
                        if i == period.weeks: #The Last Week
                            temp_weekly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=end_date).order_by('-purchased_date')
                            week['period'] = str(dt.start_of('day'))+" to "+str(end_date)
                        else:
                            temp_weekly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('week')).order_by('-purchased_date')
                            week['period'] = str(dt.start_of('day'))+" to "+str(dt.end_of('week'))
                       
                    total = temp_weekly.aggregate(Sum('amount'))
                    week['total'] = total['amount__sum']
                    data.append(week)
                    i+=1
            else: #if aggregate is monthly
                temp_start_date = start_date.start_of('month')
                period = pendulum.period(temp_start_date, end_date)
                i = 0
                for dt in period.range('months'):
                    month = {}
                    if i == 0:
                        temp_monthly =  Sales.objects.filter(purchased_date__gt=start_date.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('month')).order_by('-purchased_date')
                        month['period'] = str(start_date.start_of('day'))+" to "+str(dt.end_of('month'))
                    else:
                        if i == period.in_months():
                            temp_monthly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=end_date).order_by('-purchased_date')
                            month['period'] = str(dt.start_of('day'))+" to "+str(end_date)
                        else:
                            temp_monthly =  Sales.objects.filter(purchased_date__gt=dt.start_of('day').subtract(days=1),purchased_date__lte=dt.end_of('month')).order_by('-purchased_date')
                            month['period'] = str(dt.start_of('day'))+" to "+str(dt.end_of('month'))

                    total = temp_monthly.aggregate(Sum('amount'))
                    month['total'] = total['amount__sum']
                    data.append(month)
                    i+=1
            result.append({'request':request, 'result':data})              
            return Response(result)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)