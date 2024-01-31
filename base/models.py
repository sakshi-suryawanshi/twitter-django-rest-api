from django.db import models
from django.utils import timezone
from uuid import uuid4

class User(models.Model):
  id = models.UUIDField(primary_key = True, default=uuid4, editable=False)
  email = models.EmailField(unique = True, null=False) 
  # Add the ManyToManyField
  following = models.ManyToManyField('self', symmetrical=False, related_name="followers")


class Tweet(models.Model):
  id = models.BigAutoField(primary_key = True)
  user  = models.ForeignKey('User', on_delete=models.CASCADE)
  body = models.CharField( max_length=120, null=False) 
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  


