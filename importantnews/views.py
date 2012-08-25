from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from importantnews.forms import ReadNewsForm, AddNewsForm
from importantnews.models import News, UserRead

def unreadNews(request):
    """
    Return latest unread news.
    """
    read_news = UserRead.objects.filter(user=request.user).values_list('news__id', flat=True)
    news_list = News.objects.all().exclude(id__in=read_news).order_by('-required', '-date')
    return render_to_response('importantnews/unread-news.html', {'news_list': news_list}, RequestContext(request))


def archiveNews(request):
    """
    Return archive news.
    """
    news_list = News.objects.all().order_by('-required', '-date')
    return render_to_response('importantnews/unread-news.html', {'news_list': news_list}, RequestContext(request))


def readNews(request, pid):
    """
    Return one news and check read if news is not required
    """
    news = get_object_or_404(News, id=pid)
    if request.method == 'POST':
        form = ReadNewsForm(request.POST)
        if form.is_valid():
            try:
                UserRead.objects.get(news=news, user=request.user)
            except UserRead.DoesNotExist:
                form.save()
            return HttpResponseRedirect(reverse('unread_news'))
    else:
        form = ReadNewsForm(initial={'user': request.user, 'news': news})
    if not news.required:
        try:
            UserRead.objects.get(news=news, user=request.user)
        except UserRead.DoesNotExist:
            UserRead.objects.create(news=news, user=request.user).save()
    return render_to_response('importantnews/read-news.html', {'news': news, 'form': form}, RequestContext(request))


def addNews(request):
    """
    add new news
    """
    if request.method == "POST":
        form = AddNewsForm(request.POST)
        if form.is_valid():
            temp_news = form.save()
            return HttpResponseRedirect(reverse('read_news', args=[temp_news.id]))
        else:
            form = AddNewsForm(request.POST, request.user)
    else:
        form = AddNewsForm(initial={'author':request.user})
    return render_to_response('importantnews/add-edit-news.html', {'form': form}, RequestContext(request))


def editNews(request, pid):
    """
    edit news. Only author access
    """
    try:
        news = News.objects.get(author=request.user, id = pid)
    except News.DoesNotExist:
        raise Http404
    if request.method == "POST":
        form = AddNewsForm(request.POST, instance=news)
        if  form.is_valid():
            temp_news = form.save()
            return HttpResponseRedirect(reverse('read_news', args=[temp_news.id]))
    else:
        form = AddNewsForm(instance=news)
    return render_to_response('importantnews/add-edit-news.html', {'form': form}, RequestContext(request))