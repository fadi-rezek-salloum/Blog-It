from django.shortcuts import render
from django.db.models import Q

from articles.models import Article
from accounts.models import UserProfile

def searchArticles(request):
    queryset = Article.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'queryset': queryset,
            'user': user_profile
        }
    else:
        context = {
            'queryset': queryset,
        }

    return render(request, 'search/search-results.html', context)
