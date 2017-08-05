from rest_framework import serializers

from core.models import CodeStandardData

class CodeStandardDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeStandardData
        fields = '__all__'