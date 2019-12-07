from rest_framework import serializers

from .models import *

class PickupRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = PickupRequest
		exclude = ('user',)