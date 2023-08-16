from django.db import models
from datetime import datetime

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)

    code = models.CharField(max_length=3, blank=True, editable=False)

    def __str__(self):
        return self.name
class Bug(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Re-open', 'Re-open'),
        ('Done', 'Done'),
        ('Close', 'Close'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Add this line
    bug_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    command = models.TextField(blank=True)
    history = models.TextField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=datetime.now)

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

        # # Update the related Project's code based on the latest bug
        # if self.project:
        #     self.project.code = slugify(self.project.name)[:3].upper()
        #     self.project.save()

