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
    path('api/team/<int:pk>/', api_views.TeamListView.as_view()),
    path('api/team-list/', api_views.TeamCreateListView.as_view()),
    path('api/users-detail/<username>/', api_views.UserDetailView.as_view()),
    path('api/users/<username>/assignments/', api_views.UserAssignmentView.as_view()),
    path('api/assignment-list/', api_views.AssignmentCreateListView.as_view()),
    path('api/chore-list/', api_views.ChoreCreateListView.as_view()),
    path('api/chore-detail/<int:pk>/', api_views.ChoreDetailView.as_view()),
    path('api/assignment-detail/<int:pk>/', api_views.AssignmentDetailView.as_view()),
    path('api/point-count/<username>/', api_views.PointCountView.as_view()),
    path('api/pods/', api_views.PodCreateView.as_view()),
    path('api/pod-list/<int:pk>/', api_views.PodListView.as_view()),
    path('api/pod-detail/<int:pk>/', api_views.PodDetailView.as_view()),
    path('api/point-count/monday/<username>/', api_views.MondayPointCount.as_view()),
    path('api/point-count/tuesday/<username>/', api_views.TuesdayPointCount.as_view()),
    path('api/point-count/wednesday/<username>/', api_views.WednesdayPointCount.as_view()),
    path('api/point-count/thursday/<username>/', api_views.ThursdayPointCount.as_view()),
    path('api/point-count/friday/<username>/', api_views.FridayPointCount.as_view()),
    path('api/point-count/saturday/<username>/', api_views.SaturdayPointCount.as_view()),
    path('api/point-count/sunday/<username>/', api_views.SundayPointCount.as_view()),
    path('api/point-count/any/<username>/', api_views.AnyPointCount.as_view()),
    path('api/feeds/', api_views.FeedCreateView.as_view()),
    path('api/notifications/', api_views.NotificationCreateView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
