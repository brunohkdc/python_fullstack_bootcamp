# from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Prefetch
from posts.models import Post
from comments.models import Comment


def welcome(request):

    posts=Post.objects.all().order_by('-date_created')[:10].prefetch_related(Prefetch('comments', queryset=Comment.objects.all().order_by('-created_at')))

    return render(request, 'welcome.html', {'posts': posts})

def truncate_words(text, word_limit=40):
    """Truncate text to specified number of words"""
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return text