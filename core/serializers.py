from rest_framework import serializers

from core import models


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class CodeStandardDataSerializer(serializers.ModelSerializer):
    metadata = serializers.CharField()

    class Meta:
        model = models.CodeStandardData
        fields = ('project', 'score', 'metadata', 'report')


class CommitDataSerializer(serializers.ModelSerializer):
    metadata = serializers.CharField()

    class Meta:
        model = models.CommitData
        fields = ('data', 'email', 'username')
