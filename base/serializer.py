from rest_framework import serializers
from .models import User, Tweet

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields=('id','email')


class TweetSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField( read_only=True)
  class Meta:
    model=Tweet
    fields=('id','user', 'body', 'created_at')

