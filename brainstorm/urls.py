from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from brainstorm.models import Idea
from brainstorm.feeds import SubsiteFeed

BRAINSTORM_USE_SECRETBALLOT = getattr(settings, 'BRAINSTORM_USE_SECRETBALLOT', False)

feeds = {
    'latest': SubsiteFeed,
}

# feeds live at rss/latest/site-name/
urlpatterns = patterns('',
    url(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)

urlpatterns += patterns('brainstorm.views',
    url(r'^(?P<slug>[\w-]+)/$', 'idea_list', {'ordering': 'most_popular'}, name='ideas_popular'),
    url(r'^(?P<slug>[\w-]+)/latest/$', 'idea_list', {'ordering': 'latest'}, name='ideas_latest'),
    url(r'^(?P<slug>[\w-]+)/(?P<id>\d+)/$', 'idea_detail', name='idea_detail'),
    url(r'^(?P<slug>[\w-]+)/new_idea/$', 'new_idea', name='new_idea'),
    url(r'^vote/$', 'vote', name='idea_vote'),
)

if BRAINSTORM_USE_SECRETBALLOT:
    urlpatterns = patterns('secretballot.views',
        url(r'^vote_up/(?P<object_id>\d+)/$', 'vote',
            {'content_type': ContentType.objects.get_for_model(Idea), 'vote': 1},
              name='vote_up'),
        url(r'^vote_down/(?P<object_id>\d+)/$', 'vote',
            {'content_type': ContentType.objects.get_for_model(Idea), 'vote': -1},
              name='vote_down'),
        url(r'^unvote/(?P<object_id>\d+)/$', 'vote',
            {'content_type': ContentType.objects.get_for_model(Idea), 'vote': 0},
              name='unvote'),
    ) + urlpatterns

