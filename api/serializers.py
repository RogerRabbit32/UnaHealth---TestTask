from rest_framework import serializers
from .models import GlucoseLevel


class GlucoseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseLevel
        fields = '__all__'


class UploadCSVSerializer(serializers.Serializer):
    file = serializers.FileField(
        required=True,
    )
    user_id = serializers.IntegerField(
        required=True,
    )

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return value
