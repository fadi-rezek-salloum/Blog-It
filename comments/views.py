from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm

from accounts.models import UserProfile

@ login_required(login_url='login')
def updateComment(request, pk):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    comment = get_object_or_404(Comment, id=pk)
    article = comment.article
    c_user = request.user
    user_profile = UserProfile.objects.get(user=c_user)
    if request.user.username == comment.user.user.username:
        form = CommentForm(instance=comment)
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.instance.article = article
                form.instance.user = user_profile
                form.save()
                return HttpResponseRedirect("/articles/article-detail/{id}".format(id=comment.article.id))
        else:
            form = CommentForm(instance=comment)

    context = {
        'form': form,
        'user': user_profile
    }
    return render(request, 'articles/update-comment.html', context)


@ login_required(login_url='login')
def deleteComment(request, pk):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    comment = get_object_or_404(Comment, id=pk)
    if request.user.username == comment.user.user.username:
        comment.delete()
        return HttpResponseRedirect("/articles/article-detail/{id}".format(id=comment.article.id))
    else:
        return Http404()