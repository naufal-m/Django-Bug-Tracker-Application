from datetime import datetime
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    code = models.CharField(max_length=3, blank=True, editable=False)
    created_at = models.DateTimeField(default=datetime.now)
    users = models.ManyToManyField(User, related_name='projects')
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)[:3].upper()
        super().save(*args, **kwargs)


class Bug(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Re-open', 'Re-open'),
        ('Done', 'Done'),
        ('Closed', 'Closed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Add this line
    bug_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    reporter = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now)
    images = models.ImageField(upload_to='bug_images/', blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_bugs')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): # Generate bug ID based on project name and sequence
        if not self.bug_id:
            prefix = self.project.name[:3].upper()
            last_bug = Bug.objects.filter(project=self.project).order_by('-bug_id').first()
            if last_bug:
                last_sequence = int(last_bug.bug_id[3:]) + 1
            else:
                last_sequence = 1
            self.bug_id = f"{prefix}{str(last_sequence).zfill(3)}"

        super(Bug, self).save(*args, **kwargs)

class Image(models.Model):
    bug = models.ForeignKey('bugs.Bug', related_name='bug_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bug_images/')

    def __str__(self):
        return f"Image for Bug {self.bug.id}"

class BugHistory(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Re-open', 'Re-open'),
        ('Done', 'Done'),
        ('Closed', 'Closed'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)  # Add this line to link BugHistory to Bug
    bug_id_code = models.CharField(max_length=10, unique=False)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    updated_at = models.DateTimeField(default=datetime.now)
    status_assigned_user = models.CharField(max_length=150)  # You may want to change the field type
    report_user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming User is your user model
    images = models.ImageField(upload_to='bug_images/', blank=True, null=True)

    def __str__(self):
        return f'BugHistory for Bug {self.bug_id}'

