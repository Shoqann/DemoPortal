from django.urls import path
from . import views

urlpatterns = [
    path('api/hiring-need/', views.hiring_need_api, name='hiring_need_api'),
    path('register/', views.register_employee, name='register_employee'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.user_index, name='user_index'),
    path('logout/', views.logout_view, name='hr_logout'),
    path('leave/', views.leave_page, name='leave_page'),
    path('resignation/', views.resignation, name='resignationPage'),
    path('pension/', views.pension, name='pensionPage'),
    path('decree/', views.decree, name='decreePage'),
    path('warnings/', views.warnings, name='warningsPage'),
    path('certification/', views.certification, name='certificationPage'),
    path('other-departure/', views.other_departure, name='otherDeparturePage'),
    path('ownRequest/', views.ownRequest, name='ownReq'),
    path('AllRecords/', views.all_records, name='all_records'),
]
