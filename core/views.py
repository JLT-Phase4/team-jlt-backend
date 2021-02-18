from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response

# Create your views here.
class TestView(APIView):
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data)