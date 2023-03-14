"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.views import RegisterFormView, UserProfileView, UpdateProfileView, PasswordsChangeView, PostByUserView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", RegisterFormView.as_view(), name="register"),
    path("accounts/profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("accounts/update_profile/", UpdateProfileView.as_view(), name="update_profile"),
    path("accounts/password", PasswordsChangeView.as_view(template_name='registration/change_password.html'),
         name='change_password'),
    path("accounts/profile/post", PostByUserView.as_view(), name='post-author')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                             document_root=settings.MEDIA_ROOT)
urlpatterns +=[

    path('__debug__/', include('debug_toolbar.urls')),
]