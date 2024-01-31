from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponseBase, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Tweet
from .serializer import UserSerializer, TweetSerializer

# Create your views here.

@api_view(['GET'])
def addSampleData(request):
  if not User.objects.exists():
      # Create sample users
      user1 = User.objects.create(email="user1@example.com")
      user2 = User.objects.create(email="user2@example.com")
      user3 = User.objects.create(email="user3@example.com")
      users = User.objects.all()
      
      # Establish following relationships
      user1.following.add(user1, user2)
      user2.following.add(user2)

      tweet1 = Tweet.objects.create(
        user=user1,
        body="Hi, I am user1"
      )

      tweet2 = Tweet.objects.create(
        user=user2,
        body="Hi, I am user2"
      )


      tweet3 = Tweet.objects.create(
        user=user3,
        body="Hi, I am user3"
      )


    
  return Response({"message": "Sample Data created successfully"}, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def UserList(request):
    try:
        users = User.objects.all()   
    except User.DoesNotExist:
        return Response({"error": "User list not found"}, status=status.HTTP_404_NOT_FOUND)  
   
    serializer = UserSerializer(users, many=True)
    
    return Response(serializer.data, status= status.HTTP_200_OK)




@api_view(['GET'])
def TweetList(request):
    try:
        tweets = Tweet.objects.all()   
    except Tweet.DoesNotExist:
        return Response({"error": "Tweet list not found"}, status=status.HTTP_404_NOT_FOUND)  
   
    serializer = TweetSerializer(tweets, many=True)
    
    return Response(serializer.data, status= status.HTTP_200_OK)


# 1. createUser
@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # User created successfully
    else:
        if 'email' in serializer.errors:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # Email already in use
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Invalid input




# 2. createTweet
@api_view([ 'POST'])
def createTweet(request):
  try:
    user = User.objects.get(id=request.data["user"])
  except User.DoesNotExist:
    return Response({"error": "User not found"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)  # 405: Invalid input
    
  tweet = Tweet.objects.create(
      user=user,
      body=request.data["body"]
  )
  return Response({"message": "Tweet created successfully"}, status=status.HTTP_202_ACCEPTED)  # 202: Successful operation


# 3. get home timeline
@api_view(['GET'])
def getTweetFeed(request, id):
    try:
        user = User.objects.get(id=id)
        
    except ValueError:
        return Response({"error": "Invalid user ID supplied"}, status=status.HTTP_400_BAD_REQUEST)  # 400: Invalid user ID supplied
    except User.DoesNotExist:
        return Response({"error": "User id not found"}, status=status.HTTP_404_NOT_FOUND)  # 404: User id not found
    
    followed_users = user.following.all()
    tweets = Tweet.objects.filter(user__in=followed_users).order_by('-created_at')

    serializer = TweetSerializer(tweets, many=True)
    
    return Response(serializer.data, status= status.HTTP_200_OK)

