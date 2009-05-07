from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
import secretballot

ALLOW_ALL, REQUIRE_LOGIN, DISALLOW_ALL = range(3)
SUBSITE_POST_STATUS = (
    (ALLOW_ALL, 'Allow All Posts'),
    (REQUIRE_LOGIN, 'Require Login'),
    (DISALLOW_ALL, 'Allow No Posts'),
)

class Subsite(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    theme = models.CharField(help_text='name of base theme template', max_length=100)

    ideas_per_page = models.IntegerField(default=10)
    allow_anonymous_ideas = models.BooleanField(default=False)
    post_status = models.IntegerField(default=ALLOW_ALL, choices=SUBSITE_POST_STATUS)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subsite', args=[self.slug])

    def user_can_post(self, user):
        if self.post_status == DISALLOW_ALL:
            return False
        elif self.post_status == ALLOW_ALL:
            return True
        elif self.post_status == REQUIRE_LOGIN:
            return not user.is_anonymous()

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
