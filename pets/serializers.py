from rest_framework import serializers
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer(many=True)
    #traits = treitsSerializer(many=True)