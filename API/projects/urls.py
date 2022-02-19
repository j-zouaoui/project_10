from django.urls import path
from .views import (UserListView,
                    RegisterView,
                    ProjectListView,
                    ProjectDetailView,
                    ContributorListView,
                    ContributorDetailListView,
                    IssuesListView,
                    IssuesDetailView,
                    CommentsListView,
                    CommentsDetailView
                    )

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('signup/', RegisterView.as_view()),
    path('projects/', ProjectListView.as_view()),
    path('projects/<int:pk>/', ProjectDetailView.as_view()),
    path('projects/<int:pk>/users/', ContributorListView.as_view()),
    path('projects/<int:pk>/users/<int:id>/', ContributorDetailListView.as_view()),
    path('projects/<int:pk>/issues/', IssuesListView.as_view()),
    path('projects/<int:pk>/issues/<int:id>/', IssuesDetailView.as_view()),
    path('projects/<int:pk>/issues/<int:id>/comments/', CommentsListView.as_view()),
    path('projects/<int:pk>/issues/<int:issues_id>/comments/<int:id>/', CommentsDetailView.as_view()),
]
