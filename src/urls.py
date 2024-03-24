"""
URL configuration for src project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import hello_world, PublicEmployeeposts, PublicEmployeePostDetail


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", hello_world, name='hello_world'),
    path("job-posts/", PublicEmployeeposts.as_view(), name='alljobposts'),
    path("job-posts/<uuid:post_uid>/", PublicEmployeePostDetail.as_view(), name='viewjobpost'),
    path("auth/applicant/", include("applicants.urls")),
    path("auth/employee/", include("employees.urls")),
    path("auth/user/", include("accountio.urls")),
    # JWT Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('session/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
