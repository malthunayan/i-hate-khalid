from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView

from django.utils import timezone

from .models import *
from .serializers import *


class PickupRequestCreateView(CreateAPIView):
	serializer_class = PickupRequestSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class UserPickupHistory(ListAPIView):
	serializer_class = PickupRequestSerializer

	def get_queryset(self):
		user = self.request.user
		pickup_requests = user.pickup_requests.all().filter(
			request_on__lt=timezone.now()
		)
		return pickup_requests