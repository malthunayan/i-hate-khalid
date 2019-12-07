from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Category(models.Model):
	name = models.CharField(max_length=105)
	image = models.ImageField()

	class Meta:
		verbose_name_plural='categories'

	def __str__(self):
		return self.name


class Profile(models.Model):
	user = models.OneToOneField(
		User, related_name='profile', on_delete=models.CASCADE
	)
	points = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.user.username

	def get_profile_points(self):
		videos = self.videos.all()
		total_vote_count = sum([video.vote_count() for video in videos])
		self.points = total_vote_count
		self.save()
		return total_vote_count

def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)


class Video(models.Model):
	name = models.CharField(max_length=105)
	votes = models.ManyToManyField(User, blank=True, related_name='videos')
	youtube_url = models.CharField(max_length=105)
	category = models.ForeignKey(
		'Category', related_name='videos', on_delete=models.CASCADE
	)
	owner = models.ForeignKey(
		'Profile', related_name='videos', on_delete=models.CASCADE
	)

	def __str__(self):
		return self.name

	def vote_count(self):
		return self.votes.all().count()