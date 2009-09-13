from django.db import models
from django.contrib.auth.models import User
from pyvcs.backends import AVAILABLE_BACKENDS, get_backend
from itertools import count

LICENSE_CHOICES = (
    ("BSD", "BSD"),
    ("MIT", "MIT"),
    ("GPL", "GPL"),
    ("ARR", "All Rights Reserved"),
)

class App(models.Model):
    description = models.TextField()
    license = models.CharField(max_length=10, blank=True, choices=LICENSE_CHOICES)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, null=True, blank=True, related_name='apps_owned')
    slug = models.SlugField()
    voters = models.ManyToManyField(User, null=True, blank=True, related_name='apps_voted_for')
    website = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.name


RECORD_CATEGORIES = (
    ("commit", "Commit"),
    ("release", "Release"),
)

class Record(models.Model):
    app = models.ForeignKey(App)
    category = models.CharField(max_length=20, choices=RECORD_CATEGORIES)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    link = models.URLField()
    
    def __unicode__(self):
        return self.category + ": " + self.description[:10]


class Repository(models.Model):
    app = models.ForeignKey(App)
    repository_type = models.CharField(max_length=20, choices=AVAILABLE_BACKENDS)
    last_updated = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=150)
    
    def __unicode__(self):
        return self.get_repository_type_display() + ": " + str(self.app)
    
    @property
    def repo(self):
        if hasattr(self, '_repo'):
            return self._repo
        self._repo = get_backend(self.get_repository_type_display()).Repository(self.location)
        return self._repo

    def get_commit(self, commit_id):
        try:
            return self.repo.get_commit_by_id(str(commit_id))
        except CommitDoesNotExist:
            return None