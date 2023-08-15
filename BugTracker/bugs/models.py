from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Bug(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return self.title
