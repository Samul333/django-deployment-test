from django.urls import path 
from .views import RegisterView,LoginAPIView,VerifyEmail,UserListView,SubjectAPIView,SubjectSearchAPIView,SearchTutor,TutorDetails,RatingDetails,DeleteSubject,SessionAPIView,SessionAPIApprovedView

urlpatterns= [
    path('register/', RegisterView.as_view(), name = "register"),
    path('getUsers/', UserListView.as_view(), name="get_user"),
    path('login/', LoginAPIView.as_view(), name = "register"),
    path('email-verify/',VerifyEmail.as_view(), name='email-verify'),
    path('add-subject/',SubjectAPIView.as_view(), name='subject-api'),
    path('search/',SubjectSearchAPIView.as_view(),name='subject-search'),
    path('tutorSearch/',SearchTutor.as_view(),name='tutor-search'),
    path('tutor-details/<int:pk>/',TutorDetails,name='tutor details'),
    path('rating-list/<int:pk>/',RatingDetails,name='rating list'),
    path('delete-subject/<int:pk>/',DeleteSubject, name='delete subject'),
    path('request-session/', SessionAPIView.as_view(),name="request session"),
    path('session-approve/',SessionAPIApprovedView.as_view(),name='approve session'),
]