from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer,LoginSerializer,SubjectSerializer,TutorSerializer,UpdateSerializer,RatingsSerializer,SessionSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Subject,Ratings,Sessions
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import jwt
from django.urls import reverse
from django.conf import settings
import io
from rest_framework.decorators import api_view
from rest_framework import permissions
from .permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date


class RegisterView(generics.GenericAPIView):
    def post(self, request):
        user = request.data

        serializer = RegisterSerializer(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain

        
        relativeLink = reverse('email-verify')
        absurl = 'http://'+ current_site+relativeLink+ "?token="+ str(token)
        email_body = 'Hi ' + user.username + 'Use the link to verify your email \n'+absurl
        data = {'to_email':user.email,'email_body':email_body, 'email_subject':'Verify your email'}
      
        Util.send_email(data)
        return Response(user_data)
        
    def delete(self,request):
        json_data = request.body
        stream  = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = User.objects.get(id=id)
        stu.delete()
        res = {'msg', 'Data has been deleted!!'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')
    



class UserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user_id = request.user.id
        stu = User.objects.all().filter(id=user_id)
        serializer = TutorSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')
    def patch(self,request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = UpdateSerializer(user,data= request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        print(settings.SECRET_KEY)
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            user.is_verified = True
            user.save()
            return Response({'email':'Sucessfully activated'})
        except:
            return Response({'email':'Error validation'})

class LoginAPIView(generics.GenericAPIView):

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)



class SubjectAPIView(generics.RetrieveAPIView):
     serializer_class = SubjectSerializer
     queryset  = Subject.objects.all()
     permission_classes = [permissions.IsAuthenticated,IsOwner,]
     lookup_field ="id"
     def post(self,request):
        request.data['tutor'] = request.user.id
        serializer = SubjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data)

     def get(self,request):
        user_id = request.user.id
        subjects = Subject.objects.all().filter(tutor= user_id)
        serializer = SubjectSerializer(subjects,many=True)
        return Response(serializer.data)
    


     def perform_create(self,serializer):

        return serializer.save(tutor=self.request.user)

class SessionAPIView(generics.RetrieveAPIView):
    serializer_class = SessionSerializer
    queryset  = Sessions.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field ="id"
    def post(self,request):
        request.data['student'] = request.user.id 
        serializer = SessionSerializer(data=request.data)
        import ipdb;ipdb.set_trace() 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self,request):
        id = request.user.id
        sessions = Sessions.objects.all().filter(tutor=id).filter(is_approved=False)
        serializer = SessionSerializer(sessions,many=True)
        
        return Response(serializer.data)

class SessionAPIApprovedView(generics.RetrieveAPIView):
    serializer_class = SessionSerializer
    queryset  = Sessions.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field ="id"
    def get(self,request):
        id = request.user.id
        
        sessions = Sessions.objects.all().filter(tutor=id).filter(is_approved=True)
        serializer = SessionSerializer(sessions,many=True)
      
        return Response(serializer.data)

class SessionAPIStudentApprovedView(generics.RetrieveAPIView):
    serializer_class = SessionSerializer
    queryset  = Sessions.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field ="id"
    def get(self,request):
        id = request.user.id

        sessions = Sessions.objects.all().filter(student=id).filter(is_approved=True)
        serializer = SessionSerializer(sessions,many=True)
      
        return Response(serializer.data)

class SubjectSearchAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject_name']


class SearchTutor(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TutorSerializer


@api_view(['GET'])
def TutorDetails(request,pk):
    
    if(request.method =='GET'):
        tutor_id = pk
        tutor = User.objects.get(id=pk)
        serializer = TutorSerializer(tutor)
        return Response(serializer.data)


@api_view(['GET','POST'])
def RatingDetails(request,pk):
    
    if(request.method =='GET'):
        tutor_id = pk
        ratings = Ratings.objects.all().filter(tutor=pk)
        serializer = RatingsSerializer(ratings,many=True)
        return Response(serializer.data)
    
    if(request.method=='POST'):
        serializer = RatingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['DELETE'])
def DeleteSubject(request,pk):
    if(request.method == 'DELETE'):
        subject = Subject.objects.get(id=pk)
        subject.delete()
        return Response('Deletion Sucessful')

@api_view(['PATCH'])
def UpdateApprove(request,pk):
    if(request.method == 'PATCH'):
        sessions = Sessions.objects.get(id=pk)
        sessions.is_approved=True
        sessions.save()
        return Response('Approve Sucessful')

