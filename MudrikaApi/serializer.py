from rest_framework import serializers
from .models import Sudu, subscribers


class suduserializer(serializers.Serializer):

    class Meta:
        model = Sudu
        fields = "__all__"


class subscriberserializer(serializers.Serializer):

    class Meta:
        model = subscribers
        fields = "__all__"