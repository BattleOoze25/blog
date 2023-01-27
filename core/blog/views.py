from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . models import Blog
from . serializer import BlogSerializer
from rest_framework import status

@api_view(['GET'])

def home(request):
    blogs = Blog.objects.all()
    print(blogs)
    serializer = BlogSerializer(blogs, many=True)
    return Response({
        "message" : "Hello World",
        "data" :serializer.data
    })

@api_view(['POST'])

def create(request):

    body = request.data
    #this is vanilla method
    # obj = Blog(title = body["title"], description = body["description"])
    # obj.save()

    serializer = BlogSerializer(data = body)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])

def get_blog(request,id):
    obj = Blog.objects.filter(id=id)
    old_obj = BlogSerializer(obj[0])
    if len(obj)>0:
            serializer = BlogSerializer(obj[0])
    else:
        return Response({
        "Message": "Not Found"
        }, status = status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
    else:
        obj = obj[0]
        serializer2 = BlogSerializer(obj)
        obj.title = request.data["title"]
        obj.description = request.data["description"]
        obj.save()
        serializer = BlogSerializer(obj)
        return Response({
            "Stale data" : old_obj.data,
            "New data" : serializer.data
        }, status = status.HTTP_200_OK)

# Create your views here.
