from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self,username,email,password=None,**args):

        if username is None:
            raise TypeError('User should have username')

        if email is None:
            raise TypeError('User should have an email')
      
        user= self.model(username =username, email = self.normalize_email(email), **args)
        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self,username,email,password=None):

        if password is None:
            raise TypeError('Password should have username')

        user = self.create_user(username,email,password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff= True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=100)
    address=models.CharField(max_length=30)
    gender=models.CharField(max_length=30,)
    contactno=models.CharField(max_length=20,default=0)
    email=models.CharField(max_length=30, unique=True)
    academicLevel=models.CharField(max_length=30,blank=True)
    academicleveltoteach = models.CharField(max_length=40,blank=True,default='')
    qualification=models.CharField(max_length=100, default='', blank=True)
    educationalInstitute = models.CharField(max_length=50,default='',blank=True)
    chargePerHour=models.IntegerField(default=0, blank=True)
    is_teacher= models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return{
            'refresh':str(refresh),
            'access': str(refresh.access_token)
        }

class Tutor(models.Model):
    tutor_first_name=models.CharField(max_length=30)
    tutor_last_name=models.CharField(max_length=30)
    tutor_username=models.CharField(max_length=30)
    tutor_password=models.CharField(max_length=30)
    tutor_address=models.CharField(max_length=30)
    tutor_gender=models.CharField(max_length=30)
    tutor_contactno=models.IntegerField(default=0)
    tutor_emailaddress=models.CharField(max_length=30, unique=True)
    tutor_qualification=models.CharField(max_length=30)
    tutor_educationalInstitute=models.CharField(max_length=30)
    tutor_chargePerHour=models.IntegerField(default=0)

    def __str__(self):
        return self.tutor_first_name

class Subject(models.Model):
    tutor = models.ForeignKey(to=User,on_delete=models.PROTECT,related_name='subjects') #relationship with tutor table
    subject_name = models.CharField(max_length=30)
    

class Ratings(models.Model):
    tutor = models.ForeignKey(to=User,on_delete=models.CASCADE)
    tutor_ratings = models.CharField(max_length=30)
    tutor_review = models.CharField(max_length=100, blank=True)

class Sessions(models.Model):
    student = models.ForeignKey(to=User,on_delete=models.PROTECT, related_name='student')
    subject = models.CharField(max_length=40)
    tutor = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='tutor')
    session_date = models.CharField(max_length=50)
    session_enddate = models.CharField(max_length=40)
    message = models.CharField(max_length=100, default="")
    session_duration = models.IntegerField(default=0)
    session_days = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    

    
class Bill(models.Model):
    Payment_type=models.CharField(max_length=30)
    session_cost=models.IntegerField(default=0)
    seession = models.ForeignKey(to=Sessions, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    bill_date = models.CharField(max_length=50,default="")
 