from rest_framework import serializers

from .models import *


class VideoSerializer(serializers.ModelSerializer):
	owner = serializers.SerializerMethodField()
	votes = serializers.SerializerMethodField()

	class Meta:
		model = Video
		exclude = ('category',)

	def get_owner(self, obj):
		profile = obj.owner
		return {"profile": profile.user.username, "points": profile.get_profile_points()}

	def get_votes(self, obj):
		return obj.vote_count()


class CategorySerializer(serializers.ModelSerializer):
	videos = VideoSerializer(many=True)

	class Meta:
		model = Category
		fields = '__all__'


class VideoCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Video
		exclude = ('owner', 'votes')