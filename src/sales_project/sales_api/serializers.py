from rest_framework import serializers
from sales_api.models import AGGREGATE_CHOICE

class FilterSerializer(serializers.Serializer):
    """Serializes a start date, end date and aggregate level field for testing our APIView"""

    start_date = serializers.DateTimeField(format="%Y-%m-%d")
    end_date = serializers.DateTimeField(format="%Y-%m-%d")
    agg_level = serializers.ChoiceField(choices=AGGREGATE_CHOICE, default='daily')

