from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # dashboardpage,
     path('dashboard/', views.dashboard, name='dashboard'), 
     path('reports/', views.reports_view, name='reports'), 
     path('profile/', views.profile_view, name='profile'), 
     path('settings/', views.settings_view, name='settings'), 
     path('analytics/', views.analytics_view, name='analytics'), 
     path('schedules/', views.schedules_view, name='schedules'), 

     path('categories/', views.categories_view, name='categories'), 
     path('records/', views.records_view, name='records'), 
     path('add-records/', views.add_records_view, name='add-records'), 
     path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgotpassword/', views.forgotpassword_view, name='forgotpassword'),
]
