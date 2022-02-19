from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password

from .models import Users, Projects, Contributors, Issues, Comments

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'username']

class UserSmallDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = '__all__'

class ContributorsDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Contributors
        fields = ['id', 'user', 'permission', 'role']

class CommentsSerailizer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'

class IssuesSimplifiedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = ['id', 'title']

class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = '__all__'

class IssuesDetailSerialize(serializers.ModelSerializer):
    comment_issue = CommentsSerailizer( many=True, read_only=True)
    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project', 'status', 'created_time', 'author_user', 'comment_issue' ]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type']

class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = IssuesSimplifiedDataSerializer(many=True, read_only=True)
    project_contributor = ContributorsDetailSerializer(source="contributors", many=True, read_only=True)
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'project_contributor', 'issues']
