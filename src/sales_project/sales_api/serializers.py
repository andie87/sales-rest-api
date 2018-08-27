from rest_framework import serializers
from sales_api.models import Sales, AGGREGATE_CHOICE

class FilterSerializer(serializers.Serializer):
    """Serializes a start date, end date and aggregate level field for testing our APIView"""

    start_date = serializers.DateTimeField(format="%Y-%m-%d")
    end_date = serializers.DateTimeField(format="%Y-%m-%d")
    agg_level = serializers.ChoiceField(choices=AGGREGATE_CHOICE, default='daily')

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("end_date must occur after start_date")
        return data

class SalesSerializer(serializers.ModelSerializer):
    """Serializes a sales model."""

    user = serializers.StringRelatedField()

    class Meta:
        model = Sales
        fields = ('user', 'amount', 'purchased_date')