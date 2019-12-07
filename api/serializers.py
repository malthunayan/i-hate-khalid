from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import *


class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)
	access = serializers.CharField(allow_blank=True, read_only=True)

	class Meta:
		model = User
		fields = ('username', 'password', 'token')

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		payload = RefreshToken.for_user(new_user)
		token = str(payload.access_token)
		validated_data["token"] = token
		validated_data["access"] = token
		return validated_data



class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)
	access = serializers.CharField(allow_blank=True, read_only=True)

	def validate(self, attr):
		username = attr.get('username')
		password = attr.get('password')
		try:
			user_obj = User.objects.get(username=username)
		except User.DoesNotExist:
			error_message = "An account with this username does not exist."
			raise serializers.ValidationError({
				"username": error_message
			})
		if not user_obj.check_password(password):
			error_message = "Invalid username/password combination."
			raise serializers.ValidationError({
				"username": error_message,
				"password": error_message
			})
		payload = RefreshToken.for_user(user_obj)
		token = str(payload.access_token)
		attr["token"] = token
		attr["access"] = token
		attr["username"] = user_obj.username
		return attr


class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = '__all__'


class CriterionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Criterion
		fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
	teams = serializers.SerializerMethodField()
	project_criteria_list = serializers.SerializerMethodField()

	class Meta:
		model = Project
		exclude = ('semester', 'criteria')

	def get_teams(self, obj):
		return TeamSerializer(
			obj.teams.all().distinct(), many=True
		).data

	def get_project_criteria_list(self, obj):
		return CriterionSerializer(
			obj.criteria.all().distinct(), many=True
		).data


class SemesterSerializer(serializers.ModelSerializer):
	projects = serializers.SerializerMethodField()

	class Meta:
		model = Semester
		fields = '__all__'

	def get_projects(self, obj):
		return ProjectSerializer(obj.projects.all(), many=True).data



class ProjectModelSerializer(serializers.ModelSerializer):
	teams = serializers.SerializerMethodField()
	project_criteria_list = serializers.SerializerMethodField()
	semester = serializers.SlugRelatedField(
		queryset=Semester.objects.all(), slug_field='id'
	)

	class Meta:
		model = Project
		fields = '__all__'

	def get_teams(self, obj):
		return TeamSerializer(
			obj.teams.all().distinct(), many=True
		).data

	def get_project_criteria_list(self, obj):
		return CriterionSerializer(
			obj.criteria.all().distinct(), many=True
		).data