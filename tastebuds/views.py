from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import *
from .serializers import *


class CategoryListView(ListAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()

	def get_serializer_context(self):
		return {'request': self.request, 'user': self.request.user, 'view': self}


class VideoCreateView(CreateAPIView):
	serializer_class = VideoCreateSerializer
	permission_classes = (IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user.profile)


class VoteView(APIView):
	def post(self, request):
		user = request.user
		video_id = request.data.get('video_id')
		if video_id:
			video_obj = Video.objects.get(id=video_id)
			video_obj.votes.add(user)
			return Response("Successfully voted bro")
		return Response("Send a video id (as an integer) to vote bro")


class ProfileView(APIView):
	def get(self, request, profile_id):
		queryset = Profile.objects.all().order_by('-points')
		profile = Profile.objects.get(id=profile_id)
		ranking = list(queryset).index(profile)
		videos = profile.videos.values_list("youtube_url", flat=True)
		return Response({
			"username": profile.user.username, "points": profile.points,
			"ranking": ranking, "videos": videos
			})