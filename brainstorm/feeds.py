from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from brainstorm.models import Subsite

class SubsiteFeed(Feed):

    title_template = 'brainstorm/feed_title.html'
    description_template = 'brainstorm/feed_description.html'

    def get_object(self, bits):
        return Subsite.objects.get(slug__exact=bits[0])

    def title(self, obj):
        return 'Latest ideas submitted for %s' % obj.name

    def description(self, obj):
        return 'Latest ideas submitted for %s' % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def items(self, obj):
        return obj.ideas.order_by('-submit_date')[:30]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        return item.user

    def item_pubdate(self, item):
        return item.submit_date

