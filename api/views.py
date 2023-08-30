from django.shortcuts import render
from rest_framework.views import APIView
from .models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .throttling import customThrottle


class StudentDetails(APIView):
    queryset = Student.objects.all()   # for djangomodelpermission and djangomodelpermissionoranonreadonly, because it need to know which model should the check permisssion ,which is through the queryset or get_queryset() 
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
    def get(self,request,format=None):
        stu = Student.objects.all()
        serializer = StudentSerializer(stu,many = True)
        return Response(serializer.data)


    def post (self,request,format = None):
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'msg':'Data Created ...'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class StudentUpdates(APIView):
    queryset = Student.objects.all()   # for djangomodelpermission and djangomodelpermissionoranonreadonly, because it need to know which model should the check permisssion ,which is through the queryset or get_queryset() 
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle,customThrottle]
   
    
    def get(self,request,pk=None,format=None):
        id = pk 
        if id is not None:
            stu =Student.objects.get(pk=id)
            serializer = StudentSerializer(stu)
            return Response(serializer.data)
    
    def put(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            stu = Student.objects.get(pk=id)
            serializer = StudentSerializer(stu,data=request.data)
            if serializer.is_valid():
                serializer.save()
                res = {"msg":"Data Updated Completely"}
                data = JSONRenderer().render(res)
                return HttpResponse(data,content_type='application/json')
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self,request,pk=None,format = None):
        id = pk
        if id is not None:
            stu = Student.objects.get(pk=id)
            serializer = StudentSerializer(stu,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Data Updated Partially...'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self,request,pk=None,format=None):
        
        id= pk 
        if id is not None:
            stu = Student.objects.get(pk=id)
            stu.delete()
            return Response({'msg':'Data deleted succesfully....'})
        return Response({'msg':'Select A student...'})