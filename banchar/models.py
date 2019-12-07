from django.db import models

from django.contrib.auth.models import User


class Winch(models.Model):
	user = models.OneToOneField(
		User, related_name='winch', on_delete=models.CASCADE
	)
	current_location = models.TextField()

	def get_average_rating(self):
		ratings = self.ratings.all()
		average_rating = sum(
			ratings.values_list("stars", flat=True)
		) / len(ratings)
		return average_rating


class PickupRequest(models.Model):
	user = models.ForeignKey(
		User, related_name='pickup_requests', on_delete=models.CASCADE
	)
	location = models.TextField()
	details = models.TextField()
	winch = models.ForeignKey(
		'Winch', related_name='pickup_requests', on_delete=models.CASCADE
	)


class Rating(models.Model):
	winch = models.ForeignKey(
		'Winch', related_name='ratings', on_delete=models.CASCADE
	)
	description = models.TextField()
	stars = models.PositiveSmallIntegerField()