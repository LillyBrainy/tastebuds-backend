"""tstbuds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from API.views import UserCreateApiView,UserLoginAPIView,CreateVidoeAPIView,FilterVidoeSerializer,LikeVidoeAPIView,FilterUserVidoeSerializer,PickTwoVidoesRandomelyAPIView,UserProfileAPIView,UserBasicInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registerNewUser/', UserCreateApiView.as_view()),
    path('LoginUser/', UserLoginAPIView.as_view()),

# Vidoe ================================
	path('createVidoe/',CreateVidoeAPIView.as_view()),
	path('filterVidoe/<str:category>/',FilterVidoeSerializer.as_view()),
	path('filterUserVidoe/<int:user_id>/',FilterUserVidoeSerializer.as_view()),
	path('voteVidoe/<int:vidoe_id>/',LikeVidoeAPIView.as_view()),
	path('PickVidoeRandomly/<str:category>/',PickTwoVidoesRandomelyAPIView.as_view()),
# Profile ================================	
	path('UserBasicInfo/<int:user_id>/',UserBasicInfo.as_view()),  # to get the logged in user profile id (call it in authStore , Setuser)
	path('UserProfile/<int:profile_id>/',UserProfileAPIView.as_view()),    
]
