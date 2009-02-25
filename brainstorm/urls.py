from django.conf.urls.defaults import *
from django.contrib.contenttypes.models import ContentType
from brainstorm.models import Idea
from brainstorm.feeds import SubsiteFeed

feeds = {
    'latest': SubsiteFeed,
}

# feeds live at rss/latest/site-name/
urlpatterns = patterns('',
    url(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)

urlpatterns += patterns('brainstorm.views',
    url(r'^(?P<slug>[\w-]+)/$', 'idea_list', {'ordering': 'most_popular'}, name='subsite'),
    url(r'^(?P<slug>[\w-]+)/latest/$', 'idea_list', {'ordering': 'latest'}, name='subsite_latest'),
    url(r'^(?P<slug>[\w-]+)/(?P<id>\d+)/$', 'idea_detail', name='idea'),
    url(r'^(?P<slug>[\w-]+)/new_idea/$', 'new_idea', name='new_idea'),
)

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

