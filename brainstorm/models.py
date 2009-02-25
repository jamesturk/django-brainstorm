from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
import secretballot

class Subsite(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)

    theme = models.CharField(max_length=100)

    ideas_per_page = models.IntegerField(default=10)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subsite', args=[self.slug])

class Idea(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()

    submit_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True, related_name='ideas')
    subsite = models.ForeignKey(Subsite, related_name='ideas')

    comments = generic.GenericRelation(Comment, object_id_field='object_pk')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('idea', args=[self.subsite_id, self.id])

secretballot.enable_voting_on(Idea)
