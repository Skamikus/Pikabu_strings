from django.db import models

# Create your models here.
class posts(models.Model):
    id = models.IntegerField(primary_key=True)
    story_id = models.IntegerField(unique=True)
    href = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    story_title = models.CharField(max_length=255)
    story_block = models.TextField()
    date_in = models.DateTimeField(blank=False, auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True, blank=True)
    posted = models.BooleanField(default=False)

