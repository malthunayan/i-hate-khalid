from django.db import models


class Semester(models.Model):
	name = models.CharField(max_length=105)


class Criterion(models.Model):
	name = models.CharField(max_length=105)
	weight = models.PositiveSmallIntegerField()


class Project(models.Model):
	semester = models.ForeignKey(
		'Semester', related_name='projects', on_delete=models.CASCADE
	)
	name = models.CharField(max_length=105)
	weight = models.PositiveSmallIntegerField()
	teams = models.ManyToManyField('Team')
	criteria = models.ManyToManyField('Criterion')


class Team(models.Model):
	name = models.CharField(max_length=105)
	team_members = models.TextField()


class Judge(models.Model):
	name = models.CharField(max_length=105)


class Score(models.Model):
	criterion = models.ForeignKey(
		'Criterion', related_name='scores', on_delete=models.CASCADE
	)
	team = models.ForeignKey(
		'Team', related_name='scores', on_delete=models.CASCADE
	)
	judge = models.ForeignKey(
		'Judge', related_name='scores', on_delete=models.CASCADE
	)
	project = models.ForeignKey(
		'Project', related_name='scores', on_delete=models.CASCADE
	)
	score = models.DecimalField(max_digits=3, decimal_places=1)
	comment = models.TextField()