"""team_evaluation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views
from tastebuds import views as tasty_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('admin/', admin.site.urls),
	path('login/', views.UserLoginAPIView.as_view(), name='login'),
	path('register/', views.UserCreateAPIView.as_view(), name='register'),
	path('semester/',
		views.SemesterView.as_view({
			'get': 'list',
			'post': 'create'
		}),
		name='semester'
	),
	path('semester/<int:semester_id>/', 
		views.SemesterView.as_view({
			'get': 'retrieve',
			'put': 'update',
			'delete': 'destroy'
		}),
		name='semester-detail'
	),
	path('criterion/',
		views.CriterionView.as_view({
			'get': 'list',
			'post': 'create'
		}),
		name='criterion'
	),
	path('criterion/<int:criterion_id>/', 
		views.CriterionView.as_view({
			'get': 'retrieve',
			'put': 'update',
			'delete': 'destroy'
		}),
		name='criterion-detail'
	),
	path('project/',
		views.ProjectView.as_view({
			'get': 'list',
			'post': 'create'
		}),
		name='project'
	),
	path('project/<int:project_id>/', 
		views.ProjectView.as_view({
			'get': 'retrieve',
			'put': 'update',
			'delete': 'destroy'
		}),
		name='project-detail'
	),
	path('team/',
		views.TeamView.as_view({
			'get': 'list',
			'post': 'create'
		}),
		name='team'
	),
	path('team/<int:team_id>/', 
		views.TeamView.as_view({
			'get': 'retrieve',
			'put': 'update',
			'delete': 'destroy'
		}),
		name='team-detail'
	),
	path('score/', views.ScoreView.as_view(), name='score'),
	path('team/create/', views.TeamCreateView.as_view(), name='team-create'),
	path('judge/', views.JudgeView.as_view(), name='judge'),

	path('categories/', tasty_views.CategoryListView.as_view(), name='categories'),
	path('video/', tasty_views.VideoCreateView.as_view(), name='upload-video'),
	path('vote/', tasty_views.VoteView.as_view(), name='vote'),
]

if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)