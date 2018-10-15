import django
from django.db import models

from .models import Project, Client, ProjectClass, Comment, Finance, Achievement, Plan
def yup():
    q = Project.objects.all()
    print(q)
