from django.http import Http404
from .models import Post
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class PostList(APIView):
    'list all posts or create a new post'

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class PostDetail(APIView):
    'read, update or delete individual post'

    def get_post(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404
    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_post(pk)
        serializer = post.serializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_post(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)