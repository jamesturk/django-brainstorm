import datetime
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from brainstorm.models import Subsite, Idea

def idea_list(request, slug, ordering='-total_upvotes'):
    subsite = get_object_or_404(Subsite, pk=slug)
    ordering_db = {'most_popular': '-total_upvotes',
                   'latest': '-submit_date'}[ordering]
    paginator = Paginator(Idea.objects.from_request(request).filter(subsite=subsite).order_by(ordering_db),
                          subsite.ideas_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        ideas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ideas = paginator.page(paginator.num_pages)

    return render_to_response('brainstorm/index.html',
                              {'subsite':subsite, 'ideas': ideas,
                               'ordering': ordering,
                               'user_can_post': subsite.user_can_post(request.user)},
                              context_instance=RequestContext(request))

def idea_detail(request, slug, id):
    subsite = get_object_or_404(Subsite, pk=slug)
    idea = get_object_or_404(Idea.objects.from_request(request),
                             subsite=slug, pk=id)

    return render_to_response('brainstorm/idea.html',
                              {'subsite':subsite, 'idea': idea,
                               'user_can_post': subsite.user_can_post(request.user)},
                              context_instance=RequestContext(request))

@require_POST
def new_idea(request, slug):
    subsite = get_object_or_404(Subsite, pk=slug)
    if not subsite.user_can_post(request.user):
        return HttpResponseRedirect(subsite.get_absolute_url())
    title = request.POST['title']
    description = request.POST['description']
    if request.user.is_anonymous():
        user = None
    else:
        user = request.user
    idea = Idea.objects.create(title=title, description=description,
                               user=user, subsite=subsite)
    return HttpResponseRedirect(idea.get_absolute_url())

@require_POST
def submit_comment(request):
    from django.conf import settings
    content_type = ContentType.objects.get_for_model(Idea).id
    site = settings.SITE_ID
    object_pk = request.POST['idea_id']
    name = request.POST.get('name', 'anonymous')
    email = request.POST.get('email', '')
    url = request.POST.get('url', '')
    comment = request.POST['comment']
    date = datetime.datetime.now()
    ip = request.META['REMOTE_ADDR']
    c = Comment.objects.create(user_name=name, user_email=email, user_url=url,
            comment=comment, submit_date=date, ip_address=ip,
            site_id=site, content_type_id=content_type, object_pk=object_pk)
    idea = Idea.objects.get(pk=object_pk)
    linkback = '%s#c%s' % (idea.get_absolute_url(), c.id)
    return HttpResponseRedirect(linkback)
