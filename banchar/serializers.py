from rest_framework import serializers

from .models import *


class PickupRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = PickupRequest
		exclude = ('user',)


class WinchSerializer(serializers.ModelSerializer):
	average_ratings = serializers.SerializerMethodField()

	class Meta:
		model = Winch
		fields = '__all__'

	def get_average_ratings(self, obj):
		return obj.get_average_ratings()