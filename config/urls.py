"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include

from accounts.views import kakao_login, user_my_detail, user_detail
from schedules.views import schedule_access, schedule_single, schedule_complete
from medicines.views import medicine_access
from tags.views import tags_access
from search.views import search_medicine

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scraps/', include('scraps.urls')),
    path('auth/kakao/login', kakao_login),
    path('users/me', user_my_detail),
    path('users', user_detail),
    
    path('schedules', schedule_access),
    path('schedules/<int:id>', schedule_single),
    path('schedules/<int:id>/complete', schedule_complete),
    
    path('medicines', medicine_access),
    
    path('tags', tags_access),
    
    path('search/',search_medicine),
]