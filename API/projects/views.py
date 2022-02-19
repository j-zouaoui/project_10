from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


from .models import Users, Contributors, Projects, Issues, Comments
from .permissions import IsProjectsMember, UserPermissionObj
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProjectSerializer,
    ProjectDetailSerializer,
    ContributorsSerializer,
    ContributorsDetailSerializer,
    IssuesSerializer,
    IssuesDetailSerialize,
    CommentsSerailizer,
)

class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    #permission_classes = (AllowAny)
    serializer_class = RegisterSerializer

class ProjectListView(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    #permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

class UserListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]



class ContributorListView(generics.ListCreateAPIView):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['pk']
        return self.queryset.filter(project_id=project_id)


class ContributorDetailListView(generics.RetrieveDestroyAPIView):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsDetailSerializer
    lookup_field = 'id'
    #permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, id=None):
        item = get_object_or_404(self.queryset, project_id=pk, id=id)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

class IssuesListView(generics.ListCreateAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    #permission_classes = [IsAuthenticated]
    def get_queryset(self):
        project_id = self.kwargs['pk']
        return self.queryset.filter(project_id=project_id)


class IssuesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssuesDetailSerialize
    lookup_field = 'id'
    #permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, id=None):
        item = get_object_or_404(self.queryset, project=pk, id=id)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

class CommentsListView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerailizer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['pk']
        issues_id = self.kwargs['id']
        data = self.queryset.filter(issue=issues_id)
        results = data.filter(issue__project=project_id)
        return results



class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerailizer
    lookup_field = 'id'
    #permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, issues_id=None, id=None):
        item = get_object_or_404(self.queryset, issue_id=issues_id, id=id)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = Comments.objects.get(pk=self.kwargs["id"])
        if not request.user == comment.author_user:
            raise PermissionDenied("You can not delete this comment")
        return super().destroy(request, *args, **kwargs)

