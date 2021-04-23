from django.urls import path 
from .views import RegisterView,LoginAPIView,VerifyEmail,UserListView,SubjectAPIView,SubjectSearchAPIView,SearchTutor,TutorDetails,RatingDetails,DeleteSubject,SessionAPIView,SessionAPIApprovedView,SessionAPIStudentApprovedView, UpdateApprove, BillView,BillSView,BillDetails,UpdateBillPaidStatus,DeleteSessionRequest,PasswordTokenCheckAPI,RequestPasswordResetEmail,SetNewPasswordAPIView,MyFileView,NotificationView,RetriveMyFile

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
    path('session-approved/',SessionAPIStudentApprovedView.as_view(),name='approved session'),
    path('approve-status/<int:pk>/',UpdateApprove,name='approve status'),
    path('bill/',BillView.as_view(),name='bill'),
    path('bills/',BillSView.as_view(),name='bills'),
    path('studentclassbills/<int:pk>/',BillDetails,name='studentclassbills'),
    path('UpdateBillPaidStatus/<int:pk>/',UpdateBillPaidStatus,name='UpdateBillPaidStatus'),
    path('deleteSessionRequest/<int:pk>/',DeleteSessionRequest,name='deletesessionrequest'),
    path('password-rest/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm' ),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name='password-reset'),
    path('password-reset-complete/',SetNewPasswordAPIView.as_view(),name='password-reset-completed'),
    path('upload/',MyFileView.as_view(),name='upload-a-file'),
    path('notifications/',NotificationView.as_view(),name='notifications-user'),
    path('getFile/<int:pk>/',RetriveMyFile.as_view(),name='get-file')
]