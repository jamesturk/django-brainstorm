from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
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
                               'ordering': ordering},
                              context_instance=RequestContext(request))

def idea_detail(request, slug, id):
    subsite = get_object_or_404(Subsite, pk=slug)
    idea = get_object_or_404(Idea.objects.from_request(request),
                             subsite=slug, pk=id)

    return render_to_response('brainstorm/idea.html',
                              {'subsite':subsite, 'idea': idea},
                              context_instance=RequestContext(request))


@require_POST
def new_idea(request, slug):
    subsite = get_object_or_404(Subsite, pk=slug)
    title = request.POST['title']
    description = request.POST['description']
    if request.user.is_anonymous():
        user = None
    else:
        user = request.user

    idea = Idea.objects.create(title=title, description=description,
                               user=user, subsite=subsite)
    return HttpResponseRedirect(idea.get_absolute_url())
