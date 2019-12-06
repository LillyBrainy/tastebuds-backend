from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	points = models.IntegerField(default = 0) # Chum mara al vidoe faz
	ranking = models.IntegerField(default=0) 


	def __str__(self):
		return self.user.username

class Vidoe(models.Model):
	user = models.ForeignKey(User, on_delete= models.CASCADE)
	title = models.CharField(max_length =  800 , blank = False, null = False )
	category = models.CharField(max_length = 800, blank = False, null = False)
	number_of_voter =models.ManyToManyField(User, related_name = 'likers',  symmetrical=False)
	url = models.URLField(blank = False, null = False, default='')

	def __str__(self):
		return self.title