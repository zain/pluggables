from django.db import models
from django.contrib.auth.models import User
from codehost.hosts import CODE_HOSTS

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
    host = models.CharField(max_length=20, choices=CODE_HOSTS)
    url = models.URLField(verify_exists=False)
    
    def __unicode__(self):
        return self.app + ": " + self.get_location_display()
    
    #def post_save(self):