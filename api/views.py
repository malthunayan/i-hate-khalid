from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from django.contrib.auth.models import User
from django.db.models import Q

from .models import *
from .serializers import *


class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
	permission_classes = (AllowAny,)


class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	permission_classes = (AllowAny,)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			return Response(serializer.data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SemesterView(ModelViewSet):
	queryset = Semester.objects.all().order_by("-id")
	serializer_class = SemesterSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'semester_id'


class CriterionView(ModelViewSet):
	queryset = Criterion.objects.all()
	serializer_class = CriterionSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'criterion_id'


class ProjectView(ModelViewSet):
	queryset = Project.objects.all()
	serializer_class = ProjectModelSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'project_id'


class TeamView(ModelViewSet):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'team_id'


class ScoreView(APIView):
	def post(self, request):
		scores = []
		data = request.data
		team_id_list = data.get("team_id_list")
		project_id = data.get("project_id")
		criterion_id_list = data.get("criterion_id_list")
		for criterion_id in criterion_id_list:
			queryset = Score.objects.filter(
				Q(criterion_id=criterion_id) & Q(team_id__in=team_id_list) & Q(project_id=project_id)
			).values_list("score", flat=True)
			score = sum(list(queryset))/len(queryset)*10
			scores.append(score)
			judge_count = len(queryset)
		return Response({"scores_list": scores, "judge_count": judge_count})


class TeamCreateView(APIView):
	def post(self, request):
		data = request.data
		project_id = data.get("project_id")
		new_team = Team.objects.create(
			name=data.get("name"), team_members=data.get("team_members")
		)
		project = Project.objects.get(id=project_id)
		project.teams.add(new_team)
		return Response({
			"id": new_team.id, "name": new_team.name,
			"team_members": new_team.team_members, "project_id": project.id
		})


class JudgeView(APIView):
	def post(self, request):
		context = {"request": request}
		data = request.data
		project_id = data.get("project_id")
		project = Project.objects.get(id=project_id)
		teams = project.teams.all()
		criteria = project.criteria.all()
		serialized_criteria = CriterionSerializer(criteria, many=True, context=context).data
		serialized_teams = TeamSerializer(teams, many=True, context=context).data
		serialized_project = ProjectModelSerializer(project, context=context).data
		return Response({
			"project": serialized_project,
			"teams": serialized_teams,
			"criteria": serialized_criteria
		})