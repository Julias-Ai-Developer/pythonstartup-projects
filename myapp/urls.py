from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # homepage,
     path('home', views.home, name='home'), 
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgotpassword/', views.forgotpassword_view, name='forgotpassword'),
]
