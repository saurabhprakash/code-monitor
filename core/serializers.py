from rest_framework import serializers

from core.models import CodeStandardData


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value

class CodeStandardDataSerializer(serializers.ModelSerializer):
    metadata = serializers.CharField()
    class Meta:
        model = CodeStandardData
        fields = ('project', 'score', 'metadata', 'report')