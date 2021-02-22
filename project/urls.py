"""project URL Configuration

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
from django.conf import settings
from django.urls import include, path
from core import views
from core import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/my-profile/', views.LoggedInUserView.as_view()),
    path('api/all-users/', views.AllUserView.as_view()),
    path('api/user/<username>/', views.UserDetailView.as_view()),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/teams/', api_views.TeamList.as_view()),
    path('api/team-detail/<int:pk>/', api_views.TeamDetailView.as_view()),
    path('api/user-chore/<int:pk>/', api_views.UserChoreDetailView.as_view()),
    path('api/users/<username>/chores/', api_views.UserChoreView.as_view()),
    path('api/records/<int:pk>/', api_views.RecordDetailView.as_view()),
    path('api/records/', api_views.RecordView.as_view()),
    path('api/team/<int:pk>/', api_views.TeamListView.as_view())
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
