from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
	name=models.CharField(max_length=50)

# Create your models here.
class Post(models.Model):
	user=models.ForeignKey(User)
	date=models.DateTimeField(auto_now_add=True)
	title=models.CharField(max_length=300)
	content=models.TextField()
	votes=models.IntegerField(default=0)
	tags=models.ManyToManyField(Tag)

	#comments=models.ManyToManyField('blog.models.Comment')

class Comment(models.Model):
	user=models.ForeignKey(User)
	post=models.ForeignKey(Post)
	comm=models.ForeignKey('self',null=True, related_name='comm_set')
	date=models.DateTimeField(null=True)
	content=models.TextField()
	votes=models.IntegerField(default=0)


	                                                               
