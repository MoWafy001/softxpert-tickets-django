"""
URL configuration for support_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path("auth/", include("users.auth_urls", namespace="auth"), name="users-auth"),
    path("admin/", include("admin_console.urls", namespace="admin-console"), name="admin-console"),
    path("agents/", include("agents_console.urls", namespace="agents-console"), name="agents-console"),
]

handler404 = "tickets.views.handler404"
handler500 = "tickets.views.handle500"