import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Msg(models.Model):
	source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source',default="")
	target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target',default="")
	content = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
