from rest_framework import serializers
from .models import User,Subject,Ratings,Sessions,Bill
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode    
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode    
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from .utils import Util
class RegisterSerializer(serializers.ModelSerializer):
    password=  serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields= '__all__'

    def validate(self,attrs):
        email = attrs.get('email', '')
        username = attrs.get('username','')
        
        if not username.isalnum():
            raise serializers.ValidationError(
                'The username only contains alpha numeric character'
            )
        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields='__all__'

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3,)
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=68,read_only=True)
    class Meta:
            model = User
            fields = ['tokens','username','email','id','password','is_teacher']
    def validate(self,attrs):

        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email, password=password)

        if not user:
                raise AuthenticationFailed('Invalid credentails')

        if not user.is_verified:
            raise AuthenticationFailed('Account disabled, please activate your account')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
            'is_teacher':user.is_teacher,
        }
  



        return super().validate(attrs)

class SubjectSerializer(serializers.ModelSerializer):
    tutor_email = serializers.SerializerMethodField('get_tutor_email')
    tutor_first_name = serializers.SerializerMethodField('get_tutor_first_name')
    tutor_last_name = serializers.SerializerMethodField('get_tutor_last_name')
    tutor_academic_level = serializers.SerializerMethodField('get_tutor_academic_level')
    def get_tutor_email(self, subject_object):
        return getattr(subject_object,'tutor').email
    def get_tutor_first_name(self, subject_object):
        return getattr(subject_object,'tutor').first_name
    def get_tutor_last_name(self, subject_object):
        return getattr(subject_object,'tutor').last_name
    def get_tutor_academic_level(self, subject_object):
        return getattr(subject_object,'tutor').academicleveltoteach  
    class Meta:
        model = Subject
        fields = "__all__"

    
class TutorSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields='__all__'

class RatingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ratings
        fields='__all__'

class SessionSerializer(serializers.ModelSerializer):
    student_name= serializers.SerializerMethodField('get_student_name')
    student_lastname = serializers.SerializerMethodField('get_student_lastname')
    student_email = serializers.SerializerMethodField('get_student_email')
    tutor_chargePerHour=serializers.SerializerMethodField('get_tutor_chargePerHour')
    tutor_name= serializers.SerializerMethodField('get_tutor_name')
    tutor_lastname = serializers.SerializerMethodField('get_tutor_lastname')
    def get_student_name(self, session_object):
        return getattr(session_object,'student').first_name
    def get_student_email(self, session_object):
        return getattr(session_object,'student').email
    def get_student_lastname(self, session_object):
        return getattr(session_object,'student').last_name
    def get_tutor_name(self, session_object):
        return getattr(session_object,'tutor').first_name
    def get_tutor_lastname(self, session_object):
        return getattr(session_object,'tutor').last_name

    def get_tutor_chargePerHour(self, session_object):
        return getattr(session_object,'tutor').chargePerHour
    
    class Meta:
        model = Sessions
        fields='__all__'

class BillSerializer(serializers.ModelSerializer):
    student= serializers.SerializerMethodField('get_student')
    tutor = serializers.SerializerMethodField('get_tutor')
    def get_tutor(self, bill_object):
        tutor=getattr(bill_object,'seession').tutor
    
        return tutor.id
    def get_student(self, bill_object):
        student=getattr(bill_object,'seession').student
        return student.id
    class Meta:
        model = Bill
        fields='__all__'



class RequestPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields =['email']


class SetNewPasswordSerialzier(serializers.Serializer):
    password= serializers.CharField(min_length=6,write_only=True)
    token= serializers.CharField(min_length=1,write_only=True)
    uidb64= serializers.CharField(min_length=1,write_only=True)

    class Meta:
        fields=['password','token','uidb64']

    def validate(self,attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        return super().validate(attrs)
