from django.shortcuts import render, redirect, reverse, get_object_or_404, Http404, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import CreateArticleForm

from comments.models import Comment
from comments.forms import CommentForm

from accounts.models import UserProfile


def postDetail(request, pk):
    article = get_object_or_404(Article, id=pk)
    tags = article.tags.all()
    latest_articles = Article.objects.all().order_by('-timestamp')[0:3]
    c_user = request.user
    get_comments = Comment.objects.filter(article=article.id)
    comment_count = Comment.objects.filter(article=article.id).count()

    article.views += 1
    article.save()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=c_user)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.instance.article = article
                form.instance.user = user_profile

                form.save()
                return HttpResponseRedirect("/articles/article-detail/{id}".format(id=article.id))
        else:
            form = CommentForm()

        context = {
            'article': article,
            'tags': tags,
            'latest_articles': latest_articles,
            'form': form,
            'user': user_profile,
            'get_comments': get_comments,
            'comment_count': comment_count,
        }
    else:
        context = {
            'article': article,
            'tags': tags,
            'latest_articles': latest_articles,
            'get_comments': get_comments,
            'comment_count': comment_count,
        }

    return render(request, 'articles/blog-single.html', context)


def tagArticles(request, tag):
    tag_name = Article.tags.get(name=tag)
    articles_list = Article.objects.filter(tags=tag_name)
    paginator = Paginator(articles_list, 4)
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)


    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'tag_name': tag_name,
            'articles': articles,
            'user': user_profile
        }
    else:
        context = {
            'articles': articles,
            'tag_name': tag_name
        }
    return render(request, 'articles/tag-articles.html', context)


@login_required(login_url='login')
def postCreate(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    form = CreateArticleForm()

    c_user = request.user
    user_profile = UserProfile.objects.get(user=c_user)

    if request.method == 'POST':
        form = CreateArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = user_profile

            form.save()
            return redirect(reverse('article-detail', kwargs={"pk": form.instance.id}))
    else:
        form = CreateArticleForm()

    context = {
        'form': form,
        'user': user_profile
    }
    return render(request, 'articles/create-article.html', context)


@ login_required(login_url='login')
def postUpdate(request, pk):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    article = Article.objects.get(id=pk)

    if request.user.username == article.user.user.username:
        form = CreateArticleForm(instance=article)
        if request.method == 'POST':
            form = CreateArticleForm(
                request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect(reverse('article-detail',
                                        kwargs={"pk": form.instance.id}))
        else:
            form = CreateArticleForm(instance=article)
    else:
        return Http404()

    context = {
        'form': form,
        'user': user_profile
    }
    return render(request, 'articles/update-article.html', context)


@ login_required(login_url='login')
def postDelete(request, pk):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    article = get_object_or_404(Article, id=pk)
    if request.user.username == article.user.user.username:
        article.delete()
        return redirect('/')
    else:
        return redirect('/')
