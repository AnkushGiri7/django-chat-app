from django.urls import path
from . import views
urlpatterns = [
    path('', views.chatapp , name="chatapp" ),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
