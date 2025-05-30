from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # dashboardpage,
     path('dashboard/', views.dashboard, name='dashboard'), 
     path('records/', views.records_view, name='records'), 
     path('add-records/', views.add_records_view, name='add-records'), 
     path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgotpassword/', views.forgotpassword_view, name='forgotpassword'),
]
