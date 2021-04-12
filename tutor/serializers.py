from rest_framework import serializers
from .models import User,Subject,Ratings,Sessions
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

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
    def get_tutor_email(self, subject_object):
        return getattr(subject_object,'tutor').email
    def get_tutor_first_name(self, subject_object):
        return getattr(subject_object,'tutor').first_name
    def get_tutor_last_name(self, subject_object):
        return getattr(subject_object,'tutor').last_name
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
    student_email = serializers.SerializerMethodField('get_student_email')
    def get_student_name(self, session_object):
        return getattr(session_object,'student').first_name
    def get_student_email(self, session_object):
        return getattr(session_object,'student').email
    class Meta:
        model = Sessions
        fields='__all__'