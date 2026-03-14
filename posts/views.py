from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from posts.models import Post
from comments.models import Comment
from .forms import PostForm

from django.utils.translation import gettext_lazy as _

# Create your views here.

@login_required(login_url="login")
def all_posts(request):

    request.session['previous_url'] = request.path

    posts = Post.objects.all().order_by('-date_created').prefetch_related(Prefetch('comments', queryset=Comment.objects.all().order_by('-created_at')))
   
    return render(request, 'all_posts.html', {'posts': posts})

@login_required(login_url="login")
def my_posts(request):
 
    request.session['previous_url'] = request.path

    user_id = request.user.id
      
    posts = Post.objects.filter(user_id=user_id).order_by('-date_created').prefetch_related(Prefetch('comments', queryset=Comment.objects.all().order_by('-created_at')))
    
    return render(request, 'my_posts.html', {'posts': posts})

@login_required(login_url="login")
def my_commented_posts(request):

    request.session['previous_url'] = request.path

    user_id = request.user.id

    post_ids =  Comment.objects.filter(user_id = user_id).values_list('post_id', flat=True).distinct()

    posts = Post.objects.filter(id__in = post_ids).order_by('-date_created').prefetch_related(Prefetch('comments', queryset=Comment.objects.all().order_by('-created_at')))

    return render(request, 'my_commented_posts.html', {'posts': posts})

@login_required(login_url="login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, _('Post created successfully!'))
            return redirect('my_posts')
    else:
        form = PostForm()

    context = {
        'form': form,
        'action': 'Create',
    }
        
    return render(request, 'create_post.html', context)

@login_required
def edit_post(request, post_id):

    post = Post.objects.get(id=post_id)
    
    if post.user_id != request.user.id:
        messages.error(request, _('You don\'t have permission to edit this post.'))
        return redirect('my_posts')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, _('Post updated successfully!'))
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'action': 'Edit',
    }
    return render(request, 'edit_post.html', context)

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id, user=request.user)

    comment_count = post.comments.count()
    
    if comment_count > 0:
        post.comments.all().delete()

    post.delete()

    messages.success(request, _('Post deleted successfully!'))
    return redirect('my_posts')