from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Users(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=70, blank=True, unique=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.first_name

class Projects(models.Model):
    BACK_END = "BACK_END"
    FRONT_END = "FRONT_END"
    IOS = "IOS"
    # Define different project type
    TYPE_CHOICES = (
        (BACK_END, 'Back_end'),
        (FRONT_END, 'Front_end'),
        (IOS, 'IOS')
    )
    #author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    project_contributor = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                                 symmetrical=False, through='Contributors',
                                                 related_name='project_contributor',)

    def __str__(self):
        return self.title

class Contributors(models.Model):
    CREATOR = "CREATOR"
    RESPONSIBLE = "RESPONSIBLE"
    AUTHOR = "AUTHOR"

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (RESPONSIBLE, 'Responsable'),
        (AUTHOR,'Auteur')
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(to=Projects, related_name='contributors', on_delete=models.CASCADE, )
    permission = models.CharField(max_length=100, choices=ROLE_CHOICES, verbose_name='Rôle')
    role = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user} created {self.project}"


class Issues(models.Model):

    # Define different priority level choices variables
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    PRIORITIES_CHOICES = ((LOW, 'Faible'), (MEDIUM, 'Moyenne'), (HIGH, 'Elevée'))

    # Define a tag for each Issues
    BUG = "BUG"
    IMPROVEMENT = "IMPROVEMENT"
    TASK = "TASK"
    TAGS_CHOICES = ((BUG, 'Bug'), (IMPROVEMENT, 'Amélioration'), (TASK, 'Tâche'))

    # Define the status of each Issues
    TO_DO = "TO_DO"
    ON_GOING = "ON_GOING"
    DONE = "DONE"
    STATUS_CHOICES = ((TO_DO, 'A faire'), (ON_GOING, 'En cours'), (DONE, 'Terminer'))

    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    tag = models.CharField(max_length=100, choices=TAGS_CHOICES)
    priority = models.CharField(max_length=100, choices=PRIORITIES_CHOICES)
    project = models.ForeignKey(Projects, related_name='issues', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now=True)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_comments = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                           symmetrical=False, through='Comments', related_name='user_comments')
    # I can't use Users for both line (author_user and assignee_user)
    #assignee_user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comments(models.Model):
    description = models.CharField(max_length=200)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(to=Issues, related_name='comments', on_delete=models.CASCADE, )
    created_time = models.DateTimeField(auto_now=True)
