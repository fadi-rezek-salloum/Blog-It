from django.shortcuts import render, redirect, reverse

from accounts.models import UserProfile
from articles.models import Article
from .forms import ContactForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    articles_list = Article.objects.all().order_by('-timestamp')
        
    paginator = Paginator(articles_list, 6)
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
            'articles': articles,
            'user': user_profile,
        }
    else:
        context = {
            'articles': articles,
        }
    return render(request, 'blog/index.html', context)



def articlesList(request):
    articles_list = Article.objects.all().order_by('-timestamp')
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
            'articles': articles,
            'user': user_profile,
        }
    else:
        context = {
            'articles': articles,
        }
    return render(request, 'blog/blog.html', context)

    


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if request.user.is_authenticated:
            c_user = request.user
            user_profile = UserProfile.objects.get(user=c_user)
            form.instance.name = user_profile.user.first_name
            form.instance.email = user_profile.user.email
        if form.is_valid():
            form.save()
            return redirect(reverse('contact'))

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'form': form,
            'user': user_profile
        }
    else:
        context = {
            'form': form
        }

    return render(request, 'blog/contact.html', context)
